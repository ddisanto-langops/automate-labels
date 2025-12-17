import os
from crowdin_api import CrowdinClient

crowdin_client = CrowdinClient(token="089303ac7303cc370f40dd38ef1b4e75cd4850842d87181cb5b23eb0f370d90d089c9c5410065356")
# crowdin_client = CrowdinClient(token=os.environ.get("CROWDIN_API_KEY"))

class CrowdinLabels:
    """
    CrowdinLabels represents a list_labels request via Crowdin API 
    and provides methods for clean handling of output.
    """
    def __init__(self, project_id: int):
        try:
            labels_request = crowdin_client.labels.list_labels(projectId=project_id)
        except Exception as e:
            print(f"Error initializing CrowdinLabels class: {e}")
        
        self.project_id = project_id
        self.labels_request = labels_request
    

    def get_labels_dict(self) -> dict:
        titles = []
        ids = []
        for item in self.labels_request['data']:
            titles.append(item['data']['title'])
            ids.append(item['data']['id'])
        labels_dict = dict(zip(ids, titles))

        return labels_dict


    def get_label_titles(self) -> list:
        titles = []
        for item in self.labels_request['data']:
            titles.append(item['data']['title'])
        
        return titles
    
    def get_label_ids(self) -> list:
        ids = []
        for item in self.labels_request['data']:
            ids.append(item['data']['id'])
        
        return ids


    def check_for_uncategorized(self, label_titles: list) -> bool:
        """Checks for 'Uncategorized' label and creates if needed,
        otherwise returns the ID."""
        if "Uncategorized" in label_titles:
            return True
        else:
            return False

labels = CrowdinLabels(680084)
ids = labels.get_label_ids()
print(ids)
print(ids.index(487))