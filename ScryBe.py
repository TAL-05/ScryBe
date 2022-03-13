from Functions import edit_json, create_json, json_value, phone_alert, discord_alert
from ScribbleHub import scribble_book
from bs4 import BeautifulSoup
import cloudscraper
import time
import feedparser
import os
import re

scraper = cloudscraper.create_scraper()

if not os.path.exists('data.json'):
    with open('data.json', 'w'): pass

def scribble_update(source, toc, key, chapter, title, chapter_url):

	if key not in json_value()[source]:
		print('   Creating New Book: ' + title)
		create_json(source, key, 'new', 'new', 'new', 'new')

	if chapter not in json_value()[source][key]['chapters']:
		soup = BeautifulSoup(scraper.get(toc).text, 'html5lib')
		print("   New Chapter: " + title + ' - ' + chapter)
		
		author = str(soup.find('span', class_="auth_name_fic").get_text())
		auth_image = soup.find('img', id="acc_ava_change none")['src']
		auth_url = soup.find('span', property="name").a['href']
		image = soup.find('img', property="image")['src']
		tags = [x.text for x in soup.find_all('a', class_="fic_genre") + soup.find_all('a', id="etagme")]
		description = soup.find('div', class_="wi_fic_desc").text
		chapters = scribble_book(toc, title, author, key, chapter_url, image, tags, description)

		edit_json(source, key, 'chapters', chapters)
		edit_json(source, key, 'author', author)
		edit_json(source, key, 'title', title)
		edit_json(source, key, 'toc', toc)
		
		discord_alert(title, author, image, chapter, auth_image, auth_url, toc)
		#phone_alert(title, chapter, chapter_url, 'epub_created')

ScribbleHub = feedparser.parse("https://www.scribblehub.com/rssfeed.php?type=local&uid=7608&unq=5ca19726c44b8&lid=0")

for article in range(0,1):

	title = ScribbleHub.entries[article].category
	chapter_url = ScribbleHub.entries[article].link
	chapter = ScribbleHub.entries[article].title.split(title + ': ', 1)[1]
	series = chapter_url.split('chapter')[0].replace('read', 'series').replace('-', '/', 1)
	key = re.findall('\\d+', series)[0]

	print(title + ': ' + chapter)
	scribble_update('Scribble Hub', series, key, chapter, title.replace('’', "'").replace('â€™',"'"), chapter_url)

print('     -----Finished-----')