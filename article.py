import requests
from bs4 import BeautifulSoup


class Article:
	def __init__(self):
		self.title = ""
		self.content = []

	def get_title(self, url):

		try:
			request = requests.get(url)
			html_content = request.text
		except requests.RequestException as e:
			print(e)

		soup = BeautifulSoup(html_content, 'html.parser')

		article_title = soup.select_one("h1.heading-normal")
		article_title_stripped = article_title.get_text(strip=True).replace(" ","")
		self.title = article_title_stripped
		return self.title

	def get_content(self, url):
		
		try:
			request = requests.get(url)
			html_content = request.text
		except requests.RequestException as e:
			print(e)

		soup = BeautifulSoup(html_content, 'html.parser')
		
		article_paragraph_elements = soup.select("div.wysiwyg.article-indent p")
		
		for element in article_paragraph_elements:
			element_stripped = element.get_text(strip=True).replace(" ","")
			self.content.append(element_stripped)
		
		return self.content