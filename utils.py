import requests
from dotenv import load_dotenv
import os
import re
from bs4 import BeautifulSoup
import string

class Utils:
	def __init__(self):
		pass
	 
	def get_secret(self, key_name: str):
		try:
			load_dotenv("./secrets.env")
			KEY = os.getenv(f"{key_name}")
			return KEY
		
		except KeyError as e:
			print("Key not found. Check key name and path to .env file.")
	

	def download_file(self, url: str, download_path: str):
		request_data = requests.get(url)
		with open(download_path, mode='wb') as temp_xliff:
			for chunk in request_data.iter_content(chunk_size=8192):
				temp_xliff.write(chunk)


	def sanitize_title(self, title: str) -> str:
		"""
		Sanitizes a title by replacing commas with spaces.
		This is required by Crowdin for titles of labels.
		Ensures the title matches the regex pattern /^((?!,).)*$/.
		"""
		sanitized = re.sub(r',', ' ', title)
		return sanitized


	def normalize_text(self, text: str, remove_punctuation: bool = True) -> str:
		"""
		Normalizes text for equivalency checks.

		Args:
			text (str): Input text to normalize.
			remove_punctuation (bool): If True, removes punctuation. Default: True.

		Returns:
			str: Normalized text.
		"""
		# Convert to lowercase
		normalized = text.lower()

		# Remove punctuation if requested
		if remove_punctuation:
			normalized = normalized.translate(
				str.maketrans('', '', string.punctuation)
			)

		# Replace multiple whitespace characters with a single space
		normalized = re.sub(r'\s', '', normalized)

		# Strip leading/trailing whitespace
		normalized = normalized.strip()

		return normalized
	

	def strip_html_tags(self, html_string: str) -> str:
		"""
		Strips all HTML tags from a string using BeautifulSoup.
		"""
		soup = BeautifulSoup(html_string, "html.parser")
		return soup.get_text(separator=" ", strip=True)

