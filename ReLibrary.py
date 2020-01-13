# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from PIL import Image
import os
import datetime
import requests
import re

#Get Book Information
def relibrary_dict(url):
	soup = BeautifulSoup(requests.get(url).text, 'html5lib')
	soupDict = {
	'source' : 'Scribble Hub',
	'book' : re.findall('\d+', url)[0],
	'title' : str(soup.find('span', style=lambda value: value and value.startswith("font-size:11pt")).get_text()).split(" (", maxsplit=1)[0],
	'author': str(soup.find('span', class_="auth_name_fic").get_text()),
	'toc' : url,
	'image' : soup.find('img', property="image")['src'],
	'chapter' : soup.find('a', class_="toc_a").text
	}
	return soupDict

#Create Files
def relibrary_files(title, author, url, image):
	
	with open('metadata.txt', 'w', encoding='utf-8') as outp:
		outp.write("---\n")
		outp.write("title: "+ title.replace(':','&#58;').replace('’', "'") + "\n")
		outp.write("author: " + author.replace(':','&#58;') + "\n")
		outp.write("identifier:\n")
		outp.write("- scheme: URL\n")
		outp.write("  text: url:"+ url +"\n")
		outp.write("publisher: Re:Library\n")
		outp.write("date: "+ datetime.datetime.now().isoformat() +"\n")
		outp.write("lang: en\n")
		outp.write("cover-image: scribble.png\n")
		outp.write("stylesheet: style.css\n")
		outp.write("...\n")
	outp.close()
	Image.open(requests.get(image, stream = True).raw).save('scribble.png')
	
def decompose(tag, string, site):
	for div in site.find_all(tag, class_=string): 
		div.decompose()

def relibrary_book(url, title, author):
	with open('scribble.txt', 'w', encoding='utf-8') as outp:
			outp.close()
	soup = BeautifulSoup(requests.get(BeautifulSoup(requests.get(url).text, 'html5lib').find('a', class_="toc_a")['href']).text, 'html5lib')
	#return soup
	while True:

		chapter = soup.find('div', class_="chapter-title").text
		soup_find = soup.find('div', id="chp_contents")

		decompose('div', "ta_c_bm", soup_find)
		decompose('div', "prenext", soup_find)
		decompose('div', "pollend", soup_find)
		decompose('div', "pollstart", soup_find)
		decompose('div', "pResult", soup_find)
		decompose('li', "p_pvote", soup_find)
		decompose('div', "wi_authornotes", soup_find)
		decompose('div', "wi_news", soup_find)

		content = str(soup_find).replace('	</div>', '').replace('<hr/>', '').replace('<div class="entry-content">', '')

		with open("relibrary.txt", 'r+', encoding='utf-8') as outp:
			outp.write("\n\n# " + chapter + "\n\n")
			outp.write(content)
			outp.write('\n')
			outp.close()

		if soup.find('a', title="Shortcut: [Ctrl] + [<-]")['href'] == '#':
			break

		soup = BeautifulSoup(requests.get(soup.find('a', class_="btn-wi btn-prev")['href']).text, 'html5lib')

	#os.system('pandoc scribble.txt metadata.txt -s -o ' + '"C:/Users/thezo/Google Drive/Backup/E-Books/Scribble Hub"' + '/"' + title.replace('?','').replace(':','') + " - " + author + '.epub"')
	os.system('pandoc scribble.txt metadata.txt -s -o ' + '"C:/Users/thezo/Documents/Projects/ScryBe/Scribble Hub"' + '/"' + title.replace('?','').replace(':','') + " - " + author + '.epub"')
	os.system('rclone copy' + ' "' + title.replace('?','').replace(':','') + " - " + author + '.epub" GoogleDrive:"Backup/E-Books/Scribble Hub"')
	os.remove("metadata.txt")
	os.remove("scribble.png")
	os.remove("scribble.txt")

	return BeautifulSoup(requests.get(url).text, 'html5lib').find('a', class_="toc_a")['href']