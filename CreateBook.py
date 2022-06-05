from bs4 import BeautifulSoup
from ScribbleHub import scribble_book
import cloudscraper
import re

scraper = cloudscraper.create_scraper()

#series = input('Scribble Hub: ')
series = 'https://www.scribblehub.com/series/311259/reborn-from-the-cosmos/'

site = BeautifulSoup(scraper.get(series).text, 'html5lib')
title = site.find('div', class_="fic_title").text
author = site.find('span', class_="auth_name_fic").text
description = site.find('div', class_="wi_fic_desc").text
tags = [x.text for x in site.find_all('a', class_="fic_genre") + site.find_all('a', id="etagme")]
key = re.findall('\\d+', series)[0]
image = site.find('img', property="image")['src']
chapter_url = site.find('li', class_="toc_w").find('a')['href']

scribble_book(series, title, author, key, chapter_url, image, tags, description)