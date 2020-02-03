import datetime
from PIL import Image
import requests
import cloudscraper
import json
import os

#Edit Book Json Value
def edit_json(soruce, book, key, value):
	with open('data.json') as json_file:
		jsonData = json.load(json_file)
	jsonData[soruce][book][key] = value
	with open('data.json', 'w') as outfile:
		json.dump(jsonData, outfile, indent=4)
	return jsonData

#Get Book Json Value From Key
def json_value(soruce, book, key):
	with open('data.json') as json_file:
		jsonData = json.load(json_file)
	return jsonData[soruce][book][key]

#Create New Json Entry ForbBook
def create_json(soruce, book, author, title, toc, image, chapter, chapters):

	with open('data.json') as json_file:
		if not os.stat("data.json").st_size == 0:
			jsonData = json.load(json_file)
		else:
			jsonData = {}
	info = jsonData.get(soruce)
	if info == None:
		info = {}

	if toc not in info.keys():
		content = {'author' : author, 'title' : title, 'toc' : toc, 'image' : image, 'chapter' : chapter, 'chapters' : chapters}
		info[book] = content
		jsonData[soruce] = info

	with open('data.json', 'w') as fp:
		json.dump(jsonData, fp, indent=4)
		fp.close()

#Send Notification to Phone
def phone_alert(first, second, third, trigger):
	report = {}
	report["value1"] = first
	report["value2"] = second
	report["value3"] = third
	requests.post("https://maker.ifttt.com/trigger/" + trigger + "/with/key/YYnkWBuCxN9_1QN0uPAmt", data=report)    

#Create Metadata and Image
def create_metadata(source, title, author, url, image):
	scraper = cloudscraper.create_scraper()
	
	with open('metadata.txt', 'w', encoding='utf-8') as outp:
		outp.write("---\n")
		outp.write("title: "+ title.replace(':','&#58;') + "\n")
		outp.write("author: " + author.replace(':','&#58;') + "\n")
		outp.write("identifier:\n")
		outp.write("- scheme: URL\n")
		outp.write("  text: url:"+ url +"\n")
		outp.write("publisher: " + source + "\n")
		outp.write("date: "+ datetime.datetime.now().isoformat() +"\n")
		outp.write("lang: en\n")
		outp.write("cover-image: image.png\n")
		outp.write("stylesheet: style.css\n")
		outp.write("...\n")
	outp.close()
	Image.open(scraper.get(image, stream = True).raw).save('image.png')