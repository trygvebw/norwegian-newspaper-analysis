#!/usr/bin/env python3

import sys
import shelve
import random

from scrapers import scrapers
from common import print_headline_list

def reproject(scrapes, dest):
	for source in scrapes.keys():
		print(source)
		if not dest.get(source):
			dest[source] = {}
		for run in scrapes[source]:
			for article in run['headlines']:
				url_entry = dest[source].get(article['url'])
				if url_entry:
					url_entry['observations'].append((run['datetime'], article,))
				else:
					dest[source][article['url']] = {}
					url_entry = dest[source].get(article['url'])
					url_entry['observations'] = [(run['datetime'], article,)]
				if not url_entry.get('classes'):
					url_entry['classes'] = []

def main():
	with shelve.open('results/data', writeback=True) as data:
		with shelve.open('results/scrapes') as scrapes:
			try:
				reproject(scrapes, data)
			except KeyboardInterrupt as e:
				print('')
				pass

if __name__ == "__main__":
	main()