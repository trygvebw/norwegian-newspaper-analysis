import requests

class Scraper:
	def __init__(self, name, default_url):
		self._name = name
		self._default_url = default_url

	def get_and_scrape(self):
		response = requests.get(self.url)
		return self.scrape(response.text)

	@property
	def name(self):
		return self._name

	@property
	def default_url(self):
		return self._default_url