# -*- coding: utf-8 -*-

from Functions import edit_json, create_json, json_value, phone_alert, create_metadata
from ScribbleHub import scribble_dict, scribble_book
from NovelUpdates import novel_book, novel_dict
from bs4 import BeautifulSoup
import cfscrape
import time
import feedparser
import requests
import os
import re

if not os.path.exists('data.json'):
    with open('data.json', 'w'): pass

#Returns Book Json Data
def source_dict(source, url, string):
	if source == 'Scribble Hub':
		dictionary = scribble_dict(url)
		source = dictionary[string]
	else:
		dictionary = novel_dict(source, url, string)
		source = dictionary[string]
	return source

def check_update(url, source, book, new):

	source = source_dict(source, url, 'source')
	book = source_dict(source, url, 'book')
	author = source_dict(source, url, 'author')
	title = source_dict(source, url, 'title').replace('’', "'").replace('â€™',"'")
	toc = source_dict(source, url, 'toc')
	image = source_dict(source, url, 'image')
	chapter = source_dict(source, url, 'chapter')

	try:
		if new != json_value(source, book, 'chapter'):
			print("  New Chapter: " + title + ' - ' + new)
			create_metadata(source, title, author, url, image)
			if source == 'Scribble Hub':
				scribble_book(url, title, author)
			else:
				novel_book(source, toc, title, author, url)
			edit_json(source, book, 'chapter', new)
			phone_alert(title, new, url, 'epub_created')
			#phone_alert(title, new, image, 'epub_wear')
			print("[Chapter Updated] " + json_value(source, book, 'chapter'))
	except:
		if source == 'Scribble Hub':
			print('  Creating New Book: ' + title)
			create_json(source, book, author, title, toc, image, chapter, 'new')
			create_metadata(source, title, author, url, image)
			if source == 'Scribble Hub':
				scribble_book(url, title, author)
			else:
				print('Book Not Valid')
			phone_alert('New Book: ' + title, new, url, 'epub_created')
			#phone_alert('New Book: ' + title, new, image, 'epub_wear')
			print('Book Added')

ScribbleHub = feedparser.parse("https://www.scribblehub.com/rssfeed.php?type=global&uid=7608&unq=5ca19726c44b8")
NovelUpdates = feedparser.parse("https://www.novelupdates.com/rss.php?uid=179259&unq=5c83d5416551f&type=read")

#phone_alert("Running", "Running", "Running", 'epub_created')

while True:

	scraper = cfscrape.create_scraper()
	
	for article in range(0,0): 
		url = BeautifulSoup(scraper.get(ScribbleHub.entries[article].link).text, 'html5lib').find('div', class_='chp_byauthor').find('a')['href']
		print("start")
		new = BeautifulSoup(scraper.get(url).text, 'html5lib').find('li', title='Bookmark Chapter').find('a').text
		book = re.findall('\d+', url)[0]
		print(ScribbleHub.entries[article]['category']+': ' + new)
		check_update(url,'Scribble Hub', book, new)

	for article in range(0,25):
		description = NovelUpdates.entries[article]['description'].split(' Series Information: ')
		new = NovelUpdates.entries[article]['title']
		source = description[0].strip('()')
		url = description[-1]
		print(source + ' - ' + new)
		if source == 'Mistakes Were Made' or source == 'yurikatrans' or source == 'Re:Library':
			#print(json_value(source, url, 'toc'))
			check_update(url, source, url, BeautifulSoup(scraper.get(url).text, 'html5lib').find('a', class_="chp-release").text)

	print('Sleeping')
	break
	time.sleep(300)

#scribble_book(url, title, author)