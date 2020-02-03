from bs4 import BeautifulSoup
from Functions import json_value, edit_json, create_metadata
from PIL import Image
from natsort import natsorted
from pathlib import Path
import cloudscraper
import os
import datetime
import requests
import re

#Get Book Information
def novel_dict(source, book, string):
	novelDict = {
	'source' : source,
	'book' : book,
	'title' : json_value(source, book, 'title'),
	'author': json_value(source, book, 'author'),
	'toc' : json_value(source, book, 'toc'),
	'image' : json_value(source, book, 'image'),
	'chapter' : json_value(source, book, 'chapter')
	}
	return novelDict


def relib(source, toc, title, book):

    scraper = cloudscraper.create_scraper()

    thisdict = {}

    #print(BeautifulSoup(scraper.get(toc).text, 'html5lib'))

    for a in BeautifulSoup(scraper.get(toc).text, 'html5lib').find_all('li', class_=lambda value: value and value.startswith("page_item page-item-")):
        thisdict[a.a.text] = a.a['href']
    

    for chapter, url in thisdict.items():

        if chapter not in json_value("Re:Library", book, 'chapters'):

            soup = BeautifulSoup(scraper.get(url).text, 'html5lib')

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

            Path(re.sub(r"[^a-zA-Z0-9]+", '', source) + '/' + re.sub(r"[^a-zA-Z0-9]+", '', title) + '/').mkdir(parents=True, exist_ok=True)

            with open(re.sub(r"[^a-zA-Z0-9]+", '', source) + '/' + re.sub(r"[^a-zA-Z0-9]+", '', title) + '/' + re.sub(r"[^a-zA-Z0-9]+", '', chapter) + ".txt", 'w+', encoding='utf-8') as outp:
                outp.write("# " + chapter + "\n")
                outp.write(clean)
                outp.write('\n')             
            outp.close()

            print(' ' + chapter)

        else:
            print('Chapter Exists')
    concatFiles(source, title)
    edit_json("Re:Library", book, 'chapters', ', '.join(thisdict.keys()))
    

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
    
def mwm(toc):

    thisdict = {}

    for a in BeautifulSoup(requests.get(toc).text, 'html5lib').find_all('h2'):
        thisdict[a.a.text] = a.a['href']

    #print(thisdict)

    for chapter, url in natsorted(thisdict.items()):
    #for chapter, url in thisdict.items():
        
        soup = BeautifulSoup(requests.get(url).text, 'html5lib')

        soup_find = soup.find('div', class_="entry-content clearfix")

        for div in soup_find.find_all('img'): 
            div.replace_with(soup.new_tag('img', src=div['src']))
        
        for div in soup_find.find_all('a'): 
            div.decompose()

        for div in soup_find.find_all('div'): 
            div.decompose()

        content = str(soup_find)

        regfix = content.replace('	</div>', '').replace('<p> Next -&gt;</p>', '').replace('<div class="entry-content clearfix">', '').replace('<hr/>', '').replace('<hr/>', '').replace('<div class="post-single-content box mark-links" id="content">	', '')

        clean = re.sub('(<noscript>)(.*?)(</noscript>)', '', regfix)
        clean = re.sub('		<h\d style="text-align: center;">', '# ', clean)
        clean = re.sub('</h\d>', '\n', clean)

        with open("book.txt", 'a', encoding='utf-8') as outp:
            outp.write("# " + chapter + "\n")
            outp.write(clean)
            outp.write('\n')             
        outp.close()

        print(' ' + chapter)

def concatFiles(source, title):
    path = re.sub(r"[^a-zA-Z0-9]+", '', source) + '/' + re.sub(r"[^a-zA-Z0-9]+", '', title) + '/'
    #print("Dir " + os.listdir(path))
    files = natsorted(os.listdir(path))
    with open("book.txt", "w", encoding='utf-8') as fo: 
        for infile in files:
            with open(os.path.join(path, infile), encoding="utf8") as fin:
                for line in fin:
                    fo.write(line)

#Create Files
def novel_book(source, toc, title, author, url):
    #print(source + toc + title + author + url)
    with open('book.txt', 'w', encoding='utf-8') as outp:
            outp.close()

    if source == 'Re:Library':
        relib(source, toc, title, url)
    
    if source == 'yurikatrans':
        yurika(toc)

    if source == 'Mistakes Were Made':
        mwm(toc)


    os.system('pandoc book.txt metadata.txt -s -o ' + '"' + title.replace('?','').replace(':','') + " - " + author + '.epub"')
    #os.system('rclone copy' + ' "' + title.replace('?','').replace(':','') + " - " + author + '.epub" GoogleDrive:"Backup/E-Books/Novel Updates"')
    os.remove("metadata.txt")
    os.remove("image.png")
    os.remove("book.txt")
    #os.remove(title.replace('?','').replace(':','') + " - " + author + '.epub')

src = "Re:Library"
ttl = "Demon Sword Maiden"
table = "https://re-library.com/translations/demon-sword-maiden/"
nu = "https://www.novelupdates.com/series/demon-sword-maiden/"
au = "Carrot Sauce"
img = "https://re-library.com/wp-content/uploads/2019/07/demon-sword-maiden.png"

#create_metadata(src, ttl, au, nu, img)
#novel_book(src, table, ttl, au, nu)
