import datetime
from PIL import Image
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import cloudscraper
import json
import os

#Edit Book Json Value
def edit_json(source, book, key, value):
	with open('data.json') as json_file:
		jsonData = json.load(json_file)
	jsonData[source][book][key] = value
	with open('data.json', 'w') as outfile:
		json.dump(jsonData, outfile, indent=4)
	return jsonData

#Get Book Json Value From Key
def json_value():
	with open('data.json') as json_file:
		jsonData = json.load(json_file)
	return jsonData

#Create New Json Entry ForbBook
def create_json(source, book, author, title, toc, chapters):

	with open('data.json') as json_file:
		if not os.stat("data.json").st_size == 0:
			jsonData = json.load(json_file)
		else:
			jsonData = {}
	info = jsonData.get(source)
	if info == None:
		info = {}

	if toc not in info.keys():
		content = {'author' : author, 'title' : title, 'toc' : toc, 'chapters' : chapters}
		info[book] = content
		jsonData[source] = info

	with open('data.json', 'w') as fp:
		json.dump(jsonData, fp, indent=4)
		fp.close()

#Send Notification to Phone
def phone_alert(first, second, third, trigger):
	report = {}
	report["value1"] = first
	report["value2"] = second
	report["value3"] = third
	requests.post("https://maker.ifttt.com/trigger/" + trigger + "/with/key/c8iEn74t0TTTI8JGSmqES", data=report)    

def discord_alert(title, author, image, chapter, auth_image, auth_url, toc):
	webhook = DiscordWebhook(url='https://discord.com/api/webhooks/951217607900557352/1kDc0xW4Rv9b9elXvht4ivMMiKh7qJQfSv8i7fl8H_5L6YYIpN93o_2PqgU84FvBy7Pb')
	embed = DiscordEmbed(title=title, description = chapter, url = toc , color='03b2f8')
	embed.set_author(name=author, url = auth_url, icon_url=auth_image)
	embed.set_thumbnail(url=image)
	embed.set_timestamp()
	webhook.add_embed(embed)
	response = webhook.execute()
	