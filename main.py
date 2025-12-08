import os
from article import *
from comment import *
from xliff import *
from dotenv import load_dotenv
from webhook_example import *
from flask import Flask, request, jsonify
from crowdin_api import CrowdinClient

load_dotenv("./secrets.env")
CROWDIN_API_KEY = os.getenv("CROWDIN_API_KEY")




#app = Flask(__name__)

#@app.route('/label-request', methods=['POST'])
def label_request():
    webhook = request.json
    comment = CrowdinComment(webhook)
    project_id = comment.project_id
    
    crowdin_client = CrowdinClient(
        token= CROWDIN_API_KEY,
        project_id= project_id
    )
    
    export_file = crowdin_client.translations.export_project_translation(
    targetLanguageId= comment.target_lang,
    projectId= comment.project_id,
    format= 'xliff',
    fileIds= [comment.file_id]
)

    url = export_file['data']['url']

    xliff_request_data = requests.get(url)

    xliff_download_path = "./temp.xliff"

    with open(xliff_download_path, mode='wb') as temp_xliff:
        for chunk in xliff_request_data.iter_content(chunk_size=8192):
                temp_xliff.write(chunk)

    xliff = XLIFF(xliff_download_path)

    xliff_contents = xliff.contents
    for string in xliff_contents:
         pass

    #file_strings_no_space = file_strings.replace(" ", "")

    urls = comment.extract_urls()
    for url in urls:
        article = Article()
        article_title = article.get_title(url)
        article_content = article.get_content(url)



# TODO: init as many objects of class "Article" as required

# TODO: implement comparison logic

# TODO: implement "Add Label"

# TODO: implement "Assign Label to Strings"

#if __name__ == "__main__":
    #app.run(host="0.0.0.0", port= 5000)