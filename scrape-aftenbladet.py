#!/usr/bin/env python3

import sys
import requests
import shelve
import datetime
from pyquery import PyQuery as pq
from urllib.parse import urlparse

from common import print_headline_list, list_distinct_categories, get_article_count_by_category, print_category_count_statistics, get_base_url, is_number

URL_FILTERS = (
	'godt.no',
)

def get_aftenbladet_article_category(url):
	parsed_url = urlparse(url)
	path = parsed_url.path
	try:
		category = path.split('/')[1]

		if "podcast" in category:
			return "podcast"

		return category if not is_number(category) else None
	except IndexError:
		return None

def scrape_aftenbladet(html):
	dom = pq(html)
	headline_elements = dom('.df-blk')

	headlines = []
	for headline in headline_elements.items():
		if len(headline.parents('a')) == 0:
			print("NO A")
			continue
		url = pq(headline.parents('a')[0]).attr['href']
		text = headline.text()

		filtered_url = False
		for url_filter in URL_FILTERS:
			if url_filter in url:
				filtered_url = True
		if filtered_url:
			print("FILTERED")
			continue

		headlines.append({
			"url": url,
			"text": text,
			"category": get_aftenbladet_article_category(url)
		})
	return headlines

def get_and_scrape_aftenbladet(url):
	response = requests.get(url)
	return scrape_aftenbladet(response.text)

if __name__ == "__main__":
	if len(sys.argv) == 2:
		headlines = get_and_scrape_aftenbladet(sys.argv[1])
		print_headline_list(headlines)
		print_category_count_statistics(get_article_count_by_category(headlines))

		db_object = {
			"datetime": datetime.datetime.now(),
			"headlines": headlines
		}

		with shelve.open('scrapes', writeback=True) as db:
			if not 'aftenbladet' in db:
				db['aftenbladet'] = []
			db['aftenbladet'].append(db_object)
			print("Written to scrapes database!")
	else:
		print('Please specify url to scrape (e.g. http://aftenbladet.no)')