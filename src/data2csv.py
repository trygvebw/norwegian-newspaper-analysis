#!/usr/bin/env python3

import sys
import shelve
import csv
import random

from scrapers import scrapers
from common import print_headline_list
from sklearn.feature_extraction.text import TfidfVectorizer

def map_classes(article, metadata):
	return [1 if c in article['classes'] else 0 for c in metadata['classes']]

def map_headline(article, tfidf_model):
	return tfidf_model.transform([article['observations'][-1][1]['text']])[0].toarray().tolist()[0]

def to_csv(data, metadata):
	print('Collecting all headlines...')
	all_headlines = [data[source][k]['observations'][-1][1]['text'] for source in data.keys() for k in data[source].keys()]
	print('Done.')
	tfidf_model = TfidfVectorizer(max_df=0.95, min_df=2, max_features=1000).fit(all_headlines)
	columns = ['url', *tfidf_model.get_feature_names(), *metadata['classes']]
	for source in data.keys():
		out = []
		for k, v in data[source].items():
			headline_columns = map_headline(v, tfidf_model)
			class_columns = map_classes(v, metadata)
			if sum(class_columns) > 0:
				out.append([k, *headline_columns, *class_columns])
		with open('results/csv/{}.csv'.format(source), 'w') as f:
			writer = csv.writer(f)
			writer.writerow(columns)
			writer.writerows(out)

def main():
	with shelve.open('results/data') as data:
		with shelve.open('results/metadata') as metadata:
			try:
				to_csv(data, metadata)
			except KeyboardInterrupt as e:
				print('')
				pass

if __name__ == "__main__":
	main()