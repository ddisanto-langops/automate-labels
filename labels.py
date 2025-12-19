class CrowdinLabels:
    """
    Requires CrowdinClient from crowdin_api.
    """
    def __init__(self, crowdin_client, project_id: int):
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