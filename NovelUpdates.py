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


def relib(toc):

    thisdict = {}

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

def yurika(toc):

    thisdict = {}

    for a in BeautifulSoup(requests.get(toc).text, 'html5lib').find_all('tr'):
        thisdict[a.td.a.text] = a.td.a['href']

    #for chapter, url in natsorted(thisdict.items()):
    for chapter, url in thisdict.items():
        
        soup = BeautifulSoup(requests.get(url).text, 'html5lib')

        soup_find = soup.find('div', class_="post-single-content box mark-links")

        for div in soup_find.find_all('span', class_=lambda value: value and value.startswith("ezoic")): 
            div.decompose()

        for div in soup_find.find_all('div', class_="adboxarea"): 
            div.decompose()

        for div in soup_find.find_all(id="quarts"): 
            div.decompose()

        for div in soup_find.find_all('div', class_="tags"): 
            div.decompose()

        for div in soup_find.find_all('div', class_=lambda value: value and value.startswith("wpnm-button")): 
            div.decompose()

        for div in soup_find.find_all('br'): 
            div.decompose()

        content = str(soup_find)

        regfix = content.replace('	</div>', '').replace('<hr/>', '').replace('<div class="post-single-content box mark-links" id="content">	', '')

        clean = re.sub('(<!--)(.*?)(-->)', '', regfix)

        with open("book.txt", 'a', encoding='utf-8') as outp:
            outp.write("# " + chapter + "\n")
            outp.write(clean)
            outp.write('\n')             
        outp.close()

        print(' ' + chapter)


#Create Files
def novel_book(source, toc, title, author):

    with open('book.txt', 'w', encoding='utf-8') as outp:
            outp.close()

    if source == 'relibrary':
        relib(toc)
    
    if source == 'yurikatrans':
        yurika(toc)

    os.system('pandoc book.txt metadata.txt -s -o ' + '"' + title.replace('?','').replace(':','') + " - " + author + '.epub"')
    os.system('rclone copy' + ' "' + title.replace('?','').replace(':','') + " - " + author + '.epub" GoogleDrive:"Backup/E-Books/Novel Updates"')
    os.remove("metadata.txt")
    os.remove("image.png")
    os.remove("book.txt")
    os.remove(title.replace('?','').replace(':','') + " - " + author + '.epub')
