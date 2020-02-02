import json
import os
import requests
import cfscrape
from Functions import create_json
from bs4 import BeautifulSoup

toc = input("Index url: ")   

book = input('Novel Updates Url: ')

scraper = cfscrape.create_scraper()

soup = BeautifulSoup(scraper.get(toc).text, 'html5lib')

if 're-library.com' in toc:
	src = 'Re:Library'
	author = str(soup.find('a', rel="noopener noreferrer").get_text())
	title = str(soup.find('span', style=lambda value: value and value.startswith("font-size:11pt")).get_text()).split(" (", maxsplit=1)[0]
	image = soup.find('img')['src']
	chapter = 'New'
	chapters = 'New'
if  'yurikatrans.xyz' in toc:
	soup = BeautifulSoup(requests.get(book).text, 'html5lib')
	src = 'yurikatrans'
	author = soup.find('a', id="authtag").get_text()
	title = str(soup.find('div', class_='seriestitlenu').text)
	image = soup.find('img')['src']
	chapter = 'New'
	chapters = 'New'
if  'mwmtranslations.com' in toc:
	soup = BeautifulSoup(requests.get(book).text, 'html5lib')
	src = 'Mistakes Were Made'
	author = soup.find('a', id="authtag").get_text()
	title = str(soup.find('div', class_='seriestitlenu').text)
	image = soup.find('img')['src']
	chapter = 'New'
	chapters = 'New'

create_json(src, book, author, title, toc, image, chapter, chapters)