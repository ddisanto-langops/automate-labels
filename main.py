from flask import Flask, request, jsonify
from crowdin_api import CrowdinClient
from html import unescape
import os

# Import local modules (stubs provided below for completeness)
from scraper import Scraper
from comment import CrowdinComment
from xliff import XLIFF
from db_connector import DatabaseConnection
from utils import Utils

# --- Setup and Initialization ---

# Initialize the Utils class for common operations
utils = Utils() 

# WARNING: It is strongly recommended to use environment variables 
# instead of a local function call to retrieve secrets in production.
# For this example, we rely on the implementation in utils.py.
TOKEN = utils.get_secret("CROWDIN_API_KEY") 
# Check if token is available
if not TOKEN:
    print("WARNING: CROWDIN_API_KEY not set. Crowdin client will fail.")

# Initialize Crowdin Client
# Note: CrowdinClient initialization must occur only if TOKEN is available.
try:
    crowdin_client = CrowdinClient(token=TOKEN)
except Exception as e:
    print(f"Could not initialize CrowdinClient: {e}")
    crowdin_client = None # Set to None if initialization fails

# Initialize Flask application
app = Flask(__name__)

@app.route('/label-request', methods=['POST'])
def label_request():
    """
    Handles incoming Crowdin webhook requests.
    Processes the request to add labels based on comments containing "#label".
    Always returns a 200 OK status.
    """

    # Delete the temporary database when function is called
    try:
        os.remove("./temp.db")
    except Exception:
        print("temp.db not found.")
    
    # 1. Basic Request Validation
    if not request.json:
        print("Received request with no JSON payload.")
        return jsonify({"message": "Invalid request: Must be JSON"}), 400

    print("--- New Webhook Received ---")

    try:
        webhook = request.json
        comment = CrowdinComment(webhook)

        # 2. Check for Label Operation Request
        if "#label" not in comment.text:
            print(f"Comment received, but '#label' not found. Skipping processing.")
            # Successfully received the webhook, so return 200 OK immediately
            return jsonify({"message": "OK, skipped processing (no #label found)"}), 200
        
        print("Processing request with #label...")

        # 3. Export and download the relevant file from Crowdin as XLIFF
        if not crowdin_client:
             print("Crowdin Client not initialized. Cannot perform API calls.")
             # Still return 200 OK since the webhook was received
             return jsonify({"message": "Crowdin API initialization failed."}), 200
             
        export_file = crowdin_client.translations.export_project_translation(
            targetLanguageId=comment.target_lang_id,
            projectId=comment.project_id,
            format='xliff',
            fileIds=[comment.file_id]
        )
        url = export_file['data']['url']
        download_path = os.path.join(os.getcwd(), "temp.xliff") # Use os.path for portability
        utils.download_file(url, download_path)
        print(f"Downloaded XLIFF file to {download_path}")

        # 4. XLIFF object and contents
        xliff = XLIFF(download_path)
        xliff_contents = xliff.load_contents()

        # 5. Get the URLs in the comment
        urls = comment.extract_urls()
        
        database = DatabaseConnection()
        scraper = Scraper()
        
        for url in urls:
            print(f"Processing URL: {url}")
            
            # Scrape and sanitize title
            unsanitized_title = scraper.get_title(url)
            article_title_sanitized = utils.sanitize_title(unsanitized_title)
            article_title_normalized = utils.normalize_text(article_title_sanitized)
            
            # Scrape and process content
            scraper.get_content(url)
            unsanitized_contents = scraper.get_segmented_content()
            
            article_contents = []
            for line in unsanitized_contents:
                line = utils.normalize_text(line)
                article_contents.append(line)
            
            # 6. Add the title as a label to relevant Crowdin project
            add_label_req = crowdin_client.labels.add_label(
                title=article_title_sanitized,
                projectId=comment.project_id
            )
            label_id = add_label_req['data']['id']
            print(f"Created new label with ID: {label_id} and Title: {article_title_sanitized}")

            # 7. Insert title with strings into linked database
            database.insert_data(article_title_normalized, article_contents)
            
            # 8. For the current title, retrieve all the strings
            results = database.retreive_strings(article_title_normalized)
            
            # 9. Loop through strings of xliff file and assign label
            for string in xliff_contents:
                string_id = int(string['id'])
                string_unescaped = unescape(string['source'])
                string_stripped = utils.strip_html_tags(string_unescaped)
                string_normalized = utils.normalize_text(string_stripped)

                # See if a matching string is found
                if results and (string_normalized in results or string_normalized == article_title_normalized):
                    crowdin_client.labels.assign_label_to_strings(
                        labelId=label_id,
                        stringIds=[string_id],
                        projectId=comment.project_id
                    )
                    print(f"Assigned label {label_id} to string ID: {string_id}")
                    
    except Exception as e:
        # Log the full exception for debugging, but still return 200 to satisfy the webhook sender
        print(f"An error occurred during processing: {e}")
        # Note: If the error is critical (e.g., API failure), you might log it externally.
        
    # CRITICAL: Always return a Flask Response object, even on success/error in processing
    print("--- Webhook processing complete. Returning 200 OK. ---")
    return jsonify({}), 200

# Recommended: For development purposes only. 
# For production, use a WSGI server like Gunicorn/Waitress.
if __name__ == "__main__":
    # Use 127.0.0.1 for local testing, 0.0.0.0 for public access (make sure your firewall is configured)
    app.run(host="0.0.0.0", port=5000)
