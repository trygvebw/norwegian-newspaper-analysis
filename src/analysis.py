#!/usr/bin/env python3

import sys
import shelve
import random

from scrapers import scrapers
from common import print_article_data

def analyse(db):
	pass

def classify(db, metadata):
	assert len(sys.argv) >= 3
	source = sys.argv[2]
	assert source in scrapers.keys()

	if not metadata.get('classes'):
		metadata['classes'] = []

	source_data = db[source]
	if len(source_data) == 0:
		print('No data for source "{}"'.format(source))
		return
	print('Classifying article headlines for source "{}"'.format(source))

	source_run_count = len(source_data)

	while True:
		urls_in_run = len(source_data.keys())
		url_index = list(source_data.keys())[random.randrange(urls_in_run)]
		article = source_data[url_index]

		print_article_data(article)
		print('Existing classes: {}'.format(', '.join(metadata['classes'])))
		class_choices = input("Klasser (separer med komma): ").lower().split(",")
		cleaned_class_choices = [g for g in [c.strip() for c in class_choices] if g != '']
		if len(cleaned_class_choices) == 0:
			print('Ingen klasser valgt, fortsetter...')
		for class_choice in cleaned_class_choices:
			if not class_choice in metadata['classes']:
				create_class_choice = input("Klassen {} finnes ikke fra før, opprett ny klasse (y/n)? ".format(class_choice)).lower()
				if create_class_choice != 'y':
					continue
				else:
					metadata['classes'].append(class_choice)
			if not class_choice in article['classes']:
				article['classes'].append(class_choice)
				print('Satte klasse: {}'.format(class_choice))
			else:
				print('Klassen eksisterte allerede på denne artikkelen')
		print('Klasser er nå: {}'.format(", ".join(article['classes'])))

def main(command):
	with shelve.open('results/metadata', writeback=True) as metadata:
		if command == 'analyse':
			with shelve.open('results/data') as db:
				analyse(db)
		elif command == 'classify':
			with shelve.open('results/data', writeback=True) as db:
				try:
					classify(db, metadata)
				except KeyboardInterrupt as e:
					print('')
					pass

if __name__ == "__main__":
	assert len(sys.argv) >= 2
	command = sys.argv[1]
	main(command)