import requests
from crowdin_api import CrowdinClient
from dotenv import load_dotenv
import os

load_dotenv("./crowdin.env")
CROWDIN_API_KEY = os.getenv("CROWDIN_API_KEY")

crowdin_client = CrowdinClient(token = CROWDIN_API_KEY)

"""projs = crowdin_client.projects.list_projects()
for proj in projs['data']:
    name = proj['data']['name']
    id = proj['data']['id']
    print(f"Name: {name}. ID: {id}")"""

export_file = crowdin_client.translations.export_project_translation(
    targetLanguageId= "fr",
    projectId= 680084,
    format= 'xliff',
    fileIds= [7959]
)

url = export_file['data']['url']

file = requests.get(url)

with open("./temp.xliff", mode='wb') as temp_xliff:
    for chunk in file.iter_content(chunk_size=8192):
            temp_xliff.write(chunk)
