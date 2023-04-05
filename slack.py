import os
from slack_sdk import WebClient 
from slack_sdk.errors import SlackApiError
from pymongo import MongoClient
import requests
from datetime import date

client = MongoClient('localhost', 27017) 
db = client.jungle

cursor_all = db.users.find({})
all_data = []
for document in cursor_all:
    all_data.append(document)
all_data.sort(key=lambda x: x.get('total'),reverse=True)
number_one = all_data[0]['name']
starttime = date.today().strftime("%Y-%m-%d")
time = str(starttime)

token = "xoxb-5077704286977-5062165098101-cSJfUlyMj6clodM3RxDy7YaS"
channel = "#ranking-bot"
text = time + " 의 공부시간 1위는 " + number_one

requests.post("https://slack.com/api/chat.postMessage",
    headers={"Authorization": "Bearer "+token},
    data={"channel": channel,"text": text})
