from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import json
from flask import Flask, render_template,request, make_response, flash, redirect
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token)
import requests
from bs4 import BeautifulSoup
from datetime import datetime

times_bp = Blueprint('times', __name__)

client = MongoClient('localhost', 27017) 
db = client.jranking

@times_bp.route('/time/calculate', methods=['GET'])
def timeCalculate():
    token = request.cookies.get('refresh_token')
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('http://localhost:5000/studybutton',headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    # date = soup.select('#date')
    starttime = soup.select('#starttime')
    endtime = datetime.now()
    endtime = endtime.time().replace(microsecond=0)
    caltime = (endtime - starttime)
    user = db.users.find_one({'token':token})
    totaltime = user['time'] + ((caltime.seconds)//60)
    id = user['id']
    db.times.insert_one({'id':id, 'start':starttime, 'end':endtime})
    # db.times.insert_one({'id':id, 'date':date, 'start':starttime, 'end':endtime})
    db.users.update_one({'id':id},{'$set':{'total':totaltime}})
    return render_template('date.html', endtime = endtime)