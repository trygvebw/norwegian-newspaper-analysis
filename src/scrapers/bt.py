#!/usr/bin/env python3

from pyquery import PyQuery as pq
from urllib.parse import urlparse
from .scraper import Scraper
from common import print_headline_list, list_distinct_categories, get_article_count_by_category, print_category_count_statistics, get_base_url, is_number

URL_FILTERS = (
	'godt.no',
	'kundeweb.bt.no',
	'widget-list.herokuapp.com',
	'proaktiv.no'
)

class Bt(Scraper):
	def __init__(self, url=None):
		super().__init__('bt', 'http://bt.no')
		self.url = url if url else self.default_url

	def get_article_category(self, article_url):
		parsed_url = urlparse(article_url)
		path = parsed_url.path
		try:
			category = path.split('/')[1]

			if "podcast" in category:
				return "podcast"

			return category if not is_number(category) else None
		except IndexError:
			return None

	def scrape(self, html):
		dom = pq(html)
		headline_elements = dom('.df-article-content')

		headlines = []
		for headline in headline_elements.items():
			if len(pq(headline)('a')) == 0:
				continue
			url = pq(pq(headline)('a')[0]).attr['href']
			text = headline.text()

			filtered_url = False
			for url_filter in URL_FILTERS:
				if url_filter in url:
					filtered_url = True
			if filtered_url:
				continue

			headlines.append({
				"url": url,
				"text": text,
				"category": self.get_article_category(url)
			})
		return headlines