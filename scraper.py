import requests
from bs4 import BeautifulSoup
import spacy

# Load the spaCy English model (only once)
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser", "lemmatizer", "tagger"])
if "sentencizer" not in nlp.pipe_names:
    nlp.add_pipe("sentencizer")

class Scraper:
    def __init__(self):
        self.title = None
        self.segmented_content = []  # List of sentences

    
    def get_title(self, url: str) -> str:
        try:
            request = requests.get(f"{url}/print")
            html_content = request.text
        except requests.RequestException as e:
            print(e)
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.select_one("h1")
        if title:
            article_title_stripped = title.get_text(strip=True)
            self.title = article_title_stripped
            return self.title
    
    
    def get_segmented_content(self, url: str) -> list:
        try:
            request = requests.get(f"{url}/print")
            html_content = request.text
        except requests.RequestException as e:
            print(e)
            return []
        soup = BeautifulSoup(html_content, 'html.parser')

        article_paragraph_elements = soup.select("div.body")

        for element in article_paragraph_elements:
            element_stripped = element.get_text(strip=True)
            self.segmented_content.append(element_stripped)
            # Segment the paragraph into sentences using spaCy
            doc = nlp(element_stripped)
            sentences = [sent.text for sent in doc.sents]
            self.segmented_content.extend(sentences)

        return self.segmented_content