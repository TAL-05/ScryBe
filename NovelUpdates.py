from bs4 import BeautifulSoup
from Functions import json_value
from PIL import Image
from natsort import natsorted
import requests
import os
import datetime
import requests
import re

#Get Book Information
def novel_dict(source, book, string):
	scribbleDict = {
	'source' : source,
	'book' : book,
	'title' : json_value(source, book, 'title'),
	'author': json_value(source, book, 'author'),
	'toc' : json_value(source, book, 'toc'),
	'image' : json_value(source, book, 'image'),
	'chapter' : json_value(source, book, 'chapter')
	}
	return scribbleDict

#Create Files
def novel_book(toc, title, author):

    thisdict = {}

    with open('book.txt', 'w', encoding='utf-8') as outp:
            outp.close()

    for a in BeautifulSoup(requests.get(toc).text, 'html5lib').find_all('li', class_=lambda value: value and value.startswith("page_item page-item-")):
        thisdict[a.a.text] = a.a['href']

    #for chapter, url in natsorted(thisdict.items()):
    for chapter, url in thisdict.items():
        
        soup = BeautifulSoup(requests.get(url).text, 'html5lib')

        soup_find = soup.find('div', class_="entry-content")

        for div in soup_find.find_all('div', class_="su-table su-table-responsive su-table-alternate"): 
            div.decompose()
        for div in soup_find.find_all('span', class_=lambda value: value and value.startswith("ezoic")): 
            div.decompose()
        for div in soup_find.find_all('div', class_=lambda value: value and value.startswith("code-block code-block")): 
            div.decompose()
        for div in soup_find.find_all('div', style=lambda value: value and value.startswith("")): 
            div.decompose()
        for div in soup_find.find_all('p', style=lambda value: value and value.startswith("")): 
            div.decompose()
        for div in soup_find.find_all('div', class_=lambda value: value and value.startswith("sharedaddy")): 
            div.decompose()

        content = str(soup_find)

        clean = content.replace('	</div>', '').replace('<hr/>', '').replace('<div class="entry-content">', '')

        with open("book.txt", 'a', encoding='utf-8') as outp:
            outp.write("# " + chapter + "\n")
            outp.write(clean)
            outp.write('\n')             
        outp.close()

        print(' ' + chapter)

    os.system('pandoc book.txt metadata.txt -s -o ' + '"' + title.replace('?','').replace(':','') + " - " + author + '.epub"')
    os.system('rclone copy' + ' "' + title.replace('?','').replace(':','') + " - " + author + '.epub" GoogleDrive:"Backup/E-Books/Novel Updates"')
    os.remove("metadata.txt")
    os.remove("image.png")
    os.remove("book.txt")
    os.remove(title.replace('?','').replace(':','') + " - " + author + '.epub')


#novel_book('https://re-library.com/translations/succubus-sans-life-in-another-world/', 'Succubus-san’s Life in Another World', "Kashiwagi Masato")