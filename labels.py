import os
from crowdin_api import CrowdinClient

crowdin_client = CrowdinClient(token=os.environ.get("CROWDIN_API_KEY"))

def list_labels(project_id: int) -> list:
    label_titles = []
    labels_request = crowdin_client.labels.list_labels(projectId=project_id)
    for item in labels_request['data']:
        label_titles.append(item['data']['title'])
    
    return label_titles