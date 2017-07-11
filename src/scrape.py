#!/usr/bin/env python3

import sys
import datetime
import shelve

from parsers import Adressa, Bt, Aftenposten, Aftenbladet, Dagbladet, Morgenbladet
from common import print_headline_list, list_distinct_categories, get_article_count_by_category, print_category_count_statistics

def main(args):
	scraper = args['scraper'](args['url'])
	name = scraper.name
	headlines = scraper.get_and_scrape()
	print_headline_list(headlines)
	if len(headlines) > 0:
		print_category_count_statistics(get_article_count_by_category(headlines))
		db_object = {
			"datetime": datetime.datetime.now(),
			"headlines": headlines
		}

		with shelve.open('results/scrapes', writeback=True) as db:
			if not name in db:
				db[name] = []
			db[name].append(db_object)
			print("Written to scrapes database!")
	else:
		print('Did not scrape any headlines')

scrapers = {
	'aftenposten': Aftenposten,
	'bt': Bt,
	'aftenbladet': Aftenbladet,
	'dagbladet': Dagbladet,
	'morgenbladet': Morgenbladet,
	'adressa': Adressa,
}

def parse_arguments():
	args = sys.argv
	if len(args) < 2:
		print('Parameters: scraper (required), url (optional)')
		sys.exit(0)
	scraper = scrapers.get(args[1])
	if scraper == None:
		print('Invalid scraper, alternatives are: {}'.format(", ".join(scrapers.keys())))
		sys.exit(0)
	return {
		'scraper': scraper,
		'url': args[2] if len(args) >= 3 else None,
	}

if __name__ == "__main__":
	main(parse_arguments())