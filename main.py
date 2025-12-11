from scraper import *
from comment import *
from xliff import *
from db_connector import *
from utils import *
from webhook_example import *
from flask import Flask, request, jsonify
from crowdin_api import CrowdinClient
from html import unescape


utils = Utils()
TOKEN = utils.get_secret("CROWDIN_API_KEY")
crowdin_client = CrowdinClient(token= TOKEN)


#app = Flask(__name__)

#@app.route('/label-request', methods=['POST'])
def label_request(webhook): # fix after local testing so it works with Flask
    #webhook = request.json
    comment = CrowdinComment(webhook)

    # does the comment request label operation?
    if "#label" not in comment.text:
        exit()
    

    # export and download the relevant file from Crowdin as XLIFF
    export_file = crowdin_client.translations.export_project_translation(
	targetLanguageId= comment.target_lang_id,
	projectId= comment.project_id,
	format= 'xliff',
	fileIds= [comment.file_id]
    )
    url = export_file['data']['url']
    download_path = "./temp.xliff"
    utils.download_file(url, download_path)

    # XLIFF object and contents
    xliff = XLIFF(download_path)
    xliff_contents = xliff.load_contents()

    # get the urls in the comment
    urls = comment.extract_urls()

    # for url in comment, write article title and contents to database
    database = DatabaseConnection()
    scraper = Scraper()
    for url in urls:
        unsanitized_title = scraper.get_title(url)
        scraper.get_content(url)
        unsanitized_contents = scraper.get_segmented_content()
        article_title_sanitized = utils.sanitize_title(unsanitized_title)
        article_title_normalized = utils.normalize_text(article_title_sanitized)
        article_contents = []
        for line in unsanitized_contents:
            line = utils.normalize_text(line)
            article_contents.append(line)
        
        # add the title as a label to relevant Crowdin project
        add_label_req = crowdin_client.labels.add_label(
            title= unsanitized_title,
            projectId= comment.project_id
            )
        label_id = add_label_req['data']['id']

        # insert title with strings into linked database
        database.insert_data(article_title_normalized, article_contents)

        # for the current title, retrieve all the strings
        results = database.retreive_strings(article_title_normalized)

        # loop through strings of xliff file
        for string in xliff_contents:
            string_id = int(string['id'])
            string_unescaped = unescape(string['source'])
            string_stripped = utils.strip_html_tags(string_unescaped)
            string_normalized = utils.normalize_text(string_stripped)

            # See if a matching string is found
            # if so, add a label
            # match = database.string_match(string_text)
            if results:
                results = [result[0] for result in results]
                if string_normalized in results or string_normalized == article_title_normalized:
                    crowdin_client.labels.assign_label_to_strings(
                        labelId= label_id,
                        stringIds= [string_id],
                        projectId= comment.project_id
                    )
            
#if __name__ == "__main__":
    #app.run(host="0.0.0.0", port= 5000)


label_request(WEBHOOK)