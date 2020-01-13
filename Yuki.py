from PIL import Image
from bs4 import BeautifulSoup
import requests
import re
import datetime
import os
import sys
import json
from natsort import natsorted

url = input("Enter url: ")

chapter = ''

thisdict = {}

now = datetime.datetime.now()

#url = 'http://yurikatrans.xyz/daybreak-summoner-zz/'

data = requests.get(url)

soup = BeautifulSoup(data.text, 'html5lib')

soup.title.clear()

soup.body.hidden = True

soup.body.prettify()

title = str(soup.find('h1', class_='title').text)

print(title)

author = "Kaburagi Haruka"

print(author)

data = requests.get(url)

soup = BeautifulSoup(data.text, 'html5lib')

with open('reLib.txt', 'w', encoding='utf-8') as outp:
    outp.close()

#Downloads Image

image = soup.find('img', class_=lambda value: value and value.find("jetpack-lazy-image"))
if image == None:
    image = soup.find('img', style="border-radius:15px;")

image_url = 'https://cdn.novelupdates.com/images/2018/02/812VA1xxAwL.jpg'
img = Image.open(requests.get(image_url, stream = True).raw)
img.save('reLib.png')

for a in soup.find('table', class_='display').find_all('a'):
    thisdict[a.text] = a['href']

with open('metadata.txt', 'w', encoding='utf-8') as outp:

    outp.write("---\n")
    outp.write("title: "+ title + "\n")
    outp.write("author: " + author + "\n")
    outp.write("identifier:\n")
    outp.write("  text: url:"+ url +"\n")
    outp.write("  text: url:"+ "url" +"\n")
    outp.write("publisher: Re:Library\n")
    outp.write("date: "+ now.isoformat() +"\n")
    outp.write("lang: en\n")
    outp.write("cover-image: reLib.png\n")
    outp.write("stylesheet: style.css\n")
    outp.write("...\n")
    
outp.close()
print("Creating metadata.txt")

#Create Json File

data = {
     "name": title,
     "url": url,
     "author": author,
     "chapter": str(thisdict.keys())
    }
if os.path.isdir('data/') == False:
    os.mkdir('data/')

with open('data/' + title + '.json', 'w') as outfile:  
    json.dump(data, outfile, indent=4)
outfile.close()

for chapter, url in thisdict.items():
    
    data = requests.get(url)

    soup = BeautifulSoup(data.text, 'html5lib')

    soup.title.clear()

    soup.body.hidden = True

    soup_find = soup.find('div', id="content").find_all('p')
    
    content = '\n'.join(str(x) for x in soup_find)

    clean = content.replace('	</div>', '').replace('<hr/>', '').replace('<div class="entry-content">', '')
    
    if title not in chapter:
    	with open("reLib.txt", 'r+', encoding='utf-8') as outp:
    		contents = outp.read().split("\n")
    		outp.write("\n\n# " + chapter + "\n\n")
    		outp.write(clean)
    		outp.write('\n')
    	outp.close()
    	
    	print(chapter)
    	chapter = chapter
    
#Create Epub
    
print('Converting Epub')
os.system('pandoc reLib.txt metadata.txt -s -o ' + '"C:/Users/thezo/Google Drive/Backup/E-Books/ReLib"' + '/"' + title.replace('?','').replace(':','') + " - " + author + '.epub"')
os.remove("metadata.txt")
os.remove("reLib.png")
os.remove("reLib.txt")

def phone_alert(first, second, third):
    report = {}
    report["value1"] = first
    report["value2"] = second
    report["value3"] = third
    requests.post("https://maker.ifttt.com/trigger/epub_created/with/key/YYnkWBuCxN9_1QN0uPAmt", data=report)    

phone_alert(title, chapter, url)

def wear_alert(first, second, third):
    report = {}
    report["value1"] = first
    report["value2"] = second
    report["value3"] = third
    requests.post("https://maker.ifttt.com/trigger/epub_wear/with/key/YYnkWBuCxN9_1QN0uPAmt", data=report)    

#wear_alert(title, chapter, image_url)