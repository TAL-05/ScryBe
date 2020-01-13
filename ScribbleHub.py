from bs4 import BeautifulSoup
from PIL import Image
import os
import datetime
import requests
import re

#Get Book Information
def scribble_dict(url):
	soup = BeautifulSoup(requests.get(url).text, 'html5lib')
	scribbleDict = {
	'source' : 'Scribble Hub',
	'book' : re.findall('\d+', url)[0],
	'title' : str(soup.find('div', class_="fic_title").get_text()),
	'author': str(soup.find('span', class_="auth_name_fic").get_text()),
	'toc' : url,
	'image' : soup.find('img', property="image")['src'],
	'chapter' : soup.find('a', class_="toc_a").text
	}
	return scribbleDict

#Removes Unwanted Tags
def decompose(tag, string, site):
	for div in site.find_all(tag, class_=string): 
		div.decompose()

def scribble_book(url, title, author):
	with open('book.txt', 'w', encoding='utf-8') as outp:
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

		content = str(soup_find).replace('</div></div>', '').replace('<div id="chp_contents"><div class="chp_raw" id="chp_raw">', '').replace('<p> </p>', '').replace('<p></p>', '')

		with open("book.txt", 'r+', encoding='utf-8') as outp:
			old = outp.read()
			outp.seek(0)
			outp.truncate()
			outp.write("\n# " + chapter + "\n")
			outp.write('\n' + content + '\n')
			outp.write(old)
		outp.close()
		print(' ' + chapter)

		if soup.find('a', title="Shortcut: [Ctrl] + [<-]")['href'] == '#':
			break

		soup = BeautifulSoup(requests.get(soup.find('a', class_="btn-wi btn-prev")['href']).text, 'html5lib')

	os.system('pandoc book.txt metadata.txt -s -o ' + '"' + title.replace('?','').replace(':','') + " - " + author + '.epub"')
	os.system('rclone copy' + ' "' + title.replace('?','').replace(':','') + " - " + author + '.epub" GoogleDrive:"Backup/E-Books/Scribble Hub"')
	os.remove("metadata.txt")
	os.remove("image.png")
	os.remove("book.txt")
	os.remove(title.replace('?','').replace(':','') + " - " + author + '.epub')

	return BeautifulSoup(requests.get(url).text, 'html5lib').find('a', class_="toc_a")['href']