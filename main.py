import os
import logging
from html import unescape
from flask import Flask, request, jsonify
from crowdin_api import CrowdinClient
from labels import CrowdinLabels
from crowdin_api.exceptions import ValidationError
from scraper import Scraper
from webhook import StringCommentWebhook
from xliff import XLIFF
from db_connector import DBConnection
from utils import Utils
from wrappers import require_x_auth

# --- Setup and Initialization ---
SIMILARITY_THRESHOLD = 70

# Initialize Flask application
app = Flask(__name__)

# Configure logging to ensure messages are captured by Systemd/Gunicorn
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Utils class for common operations
utils = Utils()

TOKEN = os.environ.get("CROWDIN_API_KEY")
if not TOKEN:
    logging.warning("CROWDIN_API_KEY not set. Crowdin client will fail.")

# Initialize Crowdin Client if TOKEN is available
try:
    crowdin_client = CrowdinClient(token=TOKEN)
except Exception as e:
    logging.error(f"Could not initialize CrowdinClient: {e}")
    crowdin_client = None # Set to None if initialization fails


@app.route('/', methods=['POST'])
@require_x_auth
def label_request():
    """
    Handles incoming Crowdin webhook requests.
    Processes the request to add labels based on comments containing "#label".
    Always returns a 200 OK status.
    """
    
    logging.info("--- New Webhook Received ---") 

    # Delete the temporary database when function is called
    try:
        database = DBConnection()
    except Exception:
        logging.error("Failed to connect to in-memory database.")
        return jsonify({"message": "Failed to connect to in-memory database"}), 200
    
    # Check for JSON payload
    if not request.json:
        logging.error("Received request with no JSON payload.")
        return jsonify({"message": "Invalid request: Must be JSON"}), 400

    try:
        webhook = request.get_json(silent=True)
        
        # Immediate check for null payload
        if webhook is None:
            logging.error("JSON payload is None after get_json(). Check Content-Type header.")
            return jsonify({"message": "JSON payload is null"}), 400

        # init the string comment class and read data from webhook    
        comment = StringCommentWebhook()
        comment.read(webhook)


        # Check for label request
        if "#label" not in comment.text:
            logging.info(f"Comment received, but '#label' not found. Skipping processing.")
            # Successfully received the webhook, so return 200 OK immediately
            return jsonify({"message": "OK, skipped processing (no #label found)"}), 200
        else:
            logging.info(f"Request received from user: {comment.full_name} (user {comment.username}))")
        
        logging.info("Processing request with #label...")

        # --- DIAGNOSTIC LOGGING ---
        logging.info(f"Attempting Crowdin Export with:")
        logging.info(f"  Target Language ID: {comment.target_lang_id}")
        logging.info(f"  Project ID: {comment.project_id}")
        logging.info(f"  File ID: {comment.file_id}")
        # -------------------------------------

        # Export and download the relevant file from Crowdin as XLIFF
        if not crowdin_client:
             logging.error("Crowdin Client not initialized. Cannot perform API calls.")
             # Still return 200 OK since the webhook was received
             return jsonify({"message": "Crowdin API initialization failed."}), 200
             
        try:
            export_file = crowdin_client.translations.export_project_translation(
                targetLanguageId=comment.target_lang_id,
                projectId=comment.project_id,
                format='xliff',
                fileIds=[comment.file_id]
            )
        except ValidationError as ve:
            logging.error(f"Validation Error details: {ve.detail}")
            logging.info("--- Webhook processing terminated due to Crowdin API ValidationError. ---")
            return jsonify({"message": "Crowdin API failed during file build/export (Check server logs)."}), 200
        
        url = export_file['data']['url']
        download_path = os.path.join(os.getcwd(), "temp.xliff")
        utils.download_file(url, download_path)
        logging.info(f"Downloaded XLIFF file to {download_path}")

        # Get contents of XLIFF file
        xliff = XLIFF(download_path)
        xliff_contents = xliff.load_contents()

        # Get the URLs in the comment
        urls = utils.extract_urls(comment.text)

        # Init webscraper to provide data
        scraper = Scraper()

        # Make a request to list existing labels via CrowdinLabels
        crowdin_labels = CrowdinLabels(comment.project_id)

        for url in urls:
            logging.info(f"Processing URL: {url}")


            # Check for label 'Uncategorized' and create if needed
            # if exists, get its ID
            current_label_titles = crowdin_labels.get_label_titles()
            current_label_ids = crowdin_labels.get_label_ids()
            uncategorized_exists = crowdin_labels.check_for_uncategorized(current_label_titles)
            
            # get its ID and store as uncategorized_label_id
            if uncategorized_exists == True:
                label_index = current_label_titles.index("Uncategorized")
                uncategorized_id = current_label_ids[label_index]

            else:
                # create it
                add_uncategorized = crowdin_client.labels.add_label(
                    title="Uncategorized",
                    projectId=comment.project_id
                )
                uncategorized_id = add_uncategorized['data']['id']


            # Scrape, sanitize and normalize title
            unsanitized_title = scraper.get_title(url)
            article_title_sanitized = utils.sanitize_title(unsanitized_title)
            article_title_normalized = utils.normalize_text(article_title_sanitized)

            # Check for existing label. Crowdin cannot apply the same label to strings more than once, so exit with error.
            if article_title_sanitized in current_label_titles:
                logging.error(f"Error: Label with this title already exists. Exiting.")
                return jsonify({"message": "Label exists."}), 200
            else:   
                # Add the title as a label to relevant Crowdin project:
                add_label_req = crowdin_client.labels.add_label(
                title=article_title_sanitized,
                projectId=comment.project_id
                )
                label_id = add_label_req['data']['id']
                logging.info(f"Created new label with ID: {label_id} and Title: {article_title_sanitized}")
            
            # Scrape and normalize content
            unsanitized_contents = scraper.get_segmented_content(url)
            article_contents = []
            for line in unsanitized_contents:
                line = utils.normalize_text(line)
                article_contents.append(line)

            # Insert title with strings into linked database
            database.insert_data(article_title_normalized, article_contents, label_id)
                  
        
        for string in xliff_contents:

            # Get id, then clean up the string
            string_id = int(string['id'])
            string_unescaped = unescape(string['source'])
            string_stripped = utils.strip_html_tags(string_unescaped)
            string_normalized = utils.normalize_text(string_stripped)
           
            comparison = database.retreive_most_similar(SIMILARITY_THRESHOLD, string_normalized)
            comparison_similarity = comparison["similarity"]
            comparison_labelId = comparison["label_id"]
            if comparison_similarity >= SIMILARITY_THRESHOLD:
                crowdin_client.labels.assign_label_to_strings(
                labelId=comparison_labelId,
                stringIds=[string_id],
                projectId=comment.project_id
            )
                logging.info(f"Assigned label {comparison_labelId} to string ID: {string_id}")
            
            else:
                crowdin_client.labels.assign_label_to_strings(
                    labelId=uncategorized_id,
                    stringIds=[string_id],
                    projectId=comment.project_id
                )
                logging.info("No match found; labeled as 'Uncategorized'.")

    except Exception as e:
        # Log the full exception and traceback for debugging
        logging.error(f"An error occurred during processing: {e}", exc_info=True)
    
    try:
        if database:
            database.close_connection()
    except Exception as e:
        logging.info("Failed to close database.")
        
    # CRITICAL: Always return a Flask Response object, even on success/error in processing
    logging.info("--- Webhook processing complete. Returning 200 OK. ---")
    return jsonify({}), 200