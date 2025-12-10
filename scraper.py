import requests
from bs4 import BeautifulSoup

# TODO: implement hostname checker if needed to parse LSS. Use a separate function to figure out hostname or return an error.

class Scraper:
	def __init__(self):
		self.title = ""
		self.content = []

	def get_title(self, url: str) -> str:

		try:
			request = requests.get(url)
			html_content = request.text
		except requests.RequestException as e:
			print(e)

		soup = BeautifulSoup(html_content, 'html.parser')

		article_title = soup.select_one("h1.heading-normal")
		article_title_stripped = article_title.get_text(strip=True)
		self.title = article_title_stripped
		return self.title

	def get_content(self, url: str) -> list:
		
		try:
			request = requests.get(url)
			html_content = request.text
		except requests.RequestException as e:
			print(e)

		soup = BeautifulSoup(html_content, 'html.parser')
		
		article_paragraph_elements = soup.select("div.wysiwyg.article-indent p")
		
		for element in article_paragraph_elements:
			element_stripped = element.get_text(strip=True)
			self.content.append(element_stripped)
		
		return self.content