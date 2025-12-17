class StringCommentWebhook:
    def __init__(self):
        self.username = None
        self.full_name = None
        self.string_id = None
        self.file_id = None
        self.project_id = None
        self.target_lang_id = None
        self.text = None
    
    def read(self, json_object):
        self.username = json_object['comment']['user']['username']
        self.full_name = json_object['comment']['user']['fullName']
        self.string_id = int(json_object['comment']['string']['id'])
        self.file_id = int(json_object['comment']['string']['file']['id'])
        self.project_id = int(json_object['comment']['string']['project']['id'])
        self.target_lang_id = json_object['comment']['targetLanguage']['id']
        self.text = json_object['comment']['text']
    