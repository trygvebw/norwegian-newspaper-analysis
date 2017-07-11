from collections import defaultdict
from urllib.parse import urlparse

from termgraph import termgraph

GREEN = '\033[92m'
BLUE = '\033[94m'
END_COLOR = '\033[0m'

def print_headline_list(headline_list):
	for headline in headline_list:
		print(('\n%s' + ' (' + BLUE + '%s' + END_COLOR + GREEN + ')\n%s' + END_COLOR) % (headline["text"], headline["category"], headline["url"],))

def list_distinct_categories(headline_list):
	categories = []
	for headline in headline_list:
		categories.append(headline["category"])
	return set(categories)

def get_article_count_by_category(headline_list):
	category_count = defaultdict(int)
	for headline in headline_list:
		if headline["category"] == None:
			continue
		category_count[headline["category"]] += 1
	return dict(category_count)

def print_category_count_statistics(category_count):
	categories, counts = list(zip(*sorted(category_count.items(), key=lambda x: x[0])))
	termgraph(categories, counts)

def get_base_url(url):
	parsed_url = urlparse(url)
	return parsed_url.scheme + "://" + parsed_url.netloc

def is_number(s):
    try:
        complex(s)
    except ValueError:
        return False
    return True