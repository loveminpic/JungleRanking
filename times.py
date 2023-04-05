from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import json
from flask import Flask, render_template,request, make_response, flash, redirect
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token)
from datetime import datetime

times_bp = Blueprint('times', __name__)

client = MongoClient('localhost', 27017) 
db = client.jungle

@times_bp.route('/time/calculate', methods=['POST', 'GET'])
def timeCalculate():
    token = request.cookies.get('refresh_token')
    # date = request.form['date']
    starttime = request.form['starttime']
    starttimeformat = datetime.strptime(starttime, '%H:%M:%S')
    endtime = datetime.now()
    endtime = endtime.time().replace(microsecond=0)
    endtime = str(endtime)
    endtimeformat = datetime.strptime(endtime, '%H:%M:%S')
    caltime = (endtimeformat - starttimeformat)
    user = db.users.find_one({'token':token})
    totaltime = user['total'] + ((caltime.seconds)//60)
    id = user['id']
    db.times.insert_one({'id':id, 'start':starttime, 'end':endtime})
    # db.times.insert_one({'id':id, 'date':date, 'start':starttime, 'end':endtime})
    db.users.update_one({'id':id},{'$set':{'total':totaltime}})
    return render_template('date.html', starttime = starttime, endtime = endtime)