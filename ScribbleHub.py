from bs4 import BeautifulSoup
from Functions import edit_json
from ebooklib import epub
import subprocess
from PIL import Image
from datetime import datetime
import cloudscraper
import re
import os

scraper = cloudscraper.create_scraper()

css = open("style.css", "r")
style = css.read()
css.close()

def scribble_book(toc, title, author, key, chapter_url, image, tags, description):
    book = epub.EpubBook()

    book.set_identifier(key)
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)
    book.add_metadata('DC', 'publisher', 'Scribble Hub')
    book.add_metadata('DC', 'identifier', 'url:' + toc)
    book.add_metadata('DC', 'description', description)
    book.add_metadata('DC', 'date', str(datetime.now().isoformat()))

    for x in tags:
        book.add_metadata('DC', 'subject', x)

    book.add_metadata('DC', 'identifier', toc)

    Image.open(scraper.get(image, stream = True).raw).save('image.png')
    book.set_cover("image.png", open('image.png', 'rb').read())

    page = BeautifulSoup(scraper.get(chapter_url).text, 'html5lib')

    page_list = []

    while True:

        #for summary in page.find_all('div', class_=re.compile('^sp-head')):
            #summary.name = 'summary'

        #for details in page.find_all('div', class_=re.compile('sp-wrap')):
            #details.name = 'details'

        chapter = page.find('div', class_="chapter-title").text
        content = page.find('div', id="chp_raw")
        page_list.insert(0, [chapter, content])
        print(chapter)
        if page.find('a', title="Shortcut: [Ctrl] + [<-]")['href'] == '#':
            break
        chapter_url = page.find('a', class_="btn-wi btn-prev")['href']
        page = BeautifulSoup(scraper.get(chapter_url).text, 'html5lib')

    return create_epub(page_list, title, author, key, book, tags)

def create_epub(page_list, title, author, key, books, tags):
    chapter = epub.EpubHtml(title='Table of Content', file_name='toc.xhtml', lang='en')
    css = epub.EpubItem(uid="style", file_name="style/style.css", media_type="text/css", content=style)

    books.add_item(css)
    books.add_item(chapter)

    for chapters in page_list:
        chapter = epub.EpubHtml(
            title=chapters[0], file_name=key+str(page_list.index(chapters)) + '.xhtml', lang='en')
        chapter.add_item(css)
        chapter.content = '<h1>'+chapters[0]+'</h1>' + str(chapters[1])
        books.add_item(chapter)
        books.spine.append(chapter)
        books.toc.append(epub.Link(key+str(page_list.index(chapters)) + '.xhtml', chapters[0], key+str(page_list.index(chapters))))

    books.spine.insert(0, 'nav')
    books.spine.insert(0, 'cover')
    books.add_item(epub.EpubNcx())

    file_name = title.replace('?', '').replace(':', '') + " - " + author.replace('?', '').replace(':', '') + '.epub'

    epub.write_epub(file_name, books)
    os.system('ebook-meta "' + file_name + '" --to-opf metadata.opf')
    book_id = subprocess.check_output('calibredb add -m overwrite "' + file_name + '" --library-path "http://localhost:8083/#Calibre_Library" --username TAL-05 --password 2CooL123', shell=True).decode("utf-8") 
    print(re.findall("\d+", book_id)[0])
    os.system('calibredb set_metadata ' + re.findall("\d+", book_id)[0] + ' metadata.opf --library-path "http://localhost:8083/#Calibre_Library" --username TAL-05 --password 2CooL123')
    os.remove(file_name)
    os.remove("metadata.opf")
    os.remove("image.png")

    return ', '.join([item[0] for item in page_list])