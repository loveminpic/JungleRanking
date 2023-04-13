from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import json
from flask import Flask, render_template,request, make_response, flash, redirect
from flask_jwt_extended import (get_jwt_identity, jwt_required)
import datetime

times_bp = Blueprint('times', __name__)

client = MongoClient('localhost',27017)
db = client.jungle

@times_bp.route('/time', methods=['POST', 'GET'])
@jwt_required()
def timeCalculate():
    temptime = '23:59:59'
    temptime = datetime.datetime.strptime(temptime, '%H:%M:%S')
    id = get_jwt_identity()
    date = request.form['date']
    starttime = request.form['starttime']
    starttimeformat = datetime.datetime.strptime(starttime, '%H:%M:%S')
    endtime = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    enddate = str(endtime.date())
    endtime = endtime.time().replace(microsecond=0)
    endtime = str(endtime)
    endtimeformat = datetime.datetime.strptime(endtime, '%H:%M:%S')
    if date == enddate:
        caltime = (endtimeformat - starttimeformat)
    elif date < enddate:
        caltime = (temptime - starttimeformat) + endtimeformat
    user = db.users.find_one({'id':id})
    totaltime = user['total'] + ((caltime.seconds)//60)
    id = user['id']
    # db.times.insert_one({'id':id, 'start':starttime, 'end':endtime})
    db.times.insert_one({'id':id, 'date':date, 'start':starttime, 'end':endtime})
    db.users.update_one({'id':id},{'$set':{'total':totaltime}})
    return render_template('date.html', starttime = starttime, endtime = endtime, date = date)