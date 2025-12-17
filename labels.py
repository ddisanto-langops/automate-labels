import os
from crowdin_api import CrowdinClient

crowdin_client = CrowdinClient(token=os.environ.get("CROWDIN_API_KEY"))

def list_labels(project_id):
    label_ids = []
    label_titles = []
    label_dict = {}
    labels_request = crowdin_client.labels.list_labels(projectId=project_id)
    for item in labels_request['data']:
        label_ids.append(item['data']['id']) 
        label_titles.append(item['data']['title'])
    
    for id, title in zip(label_ids, label_titles):
        label_dict[id] = title
    
    return label_dict