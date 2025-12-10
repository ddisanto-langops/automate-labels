import re

class CrowdinComment:
    """
    Exepcts a webhook (see Crowdin docs) and extracts desired information
    """
    def __init__(self, webhook):
        self.text = webhook['comment']['text']
        self.project_id = webhook['comment']['string']['project']['id']
        self.file_id = webhook['comment']['string']['file']['id']
        self.string_id = webhook['comment']['string']['id']
        self.target_lang_id = webhook['comment']['targetLanguage']['id']
    
    def extract_urls(self) -> list:
        pattern = re.compile(r'\bhttps://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:[/\w .-]*)*/?[^\s.,;()]{0,20}?(?:\?[^\s]*)?(?:#[^\s]*)?')
        urls = re.findall(
            pattern= pattern,
            string= self.text
        )

        return urls
