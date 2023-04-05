from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import json
from flask import Flask, render_template,request, make_response, flash, redirect
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token)

rank_bp = Blueprint('rank', __name__)

client = MongoClient('localhost', 27017) 
db = client.jranking

@rank_bp.route('/rank', methods=['POST', 'GET']) # 'GET'
def rank():
    token = request.cookies.get('refresh_token')
    if token is not None :
        users = list(db.users.find({}, {'_id' : False}).sort('total', -1))
        user = db.users.find_one({'token':token}, {'_id' : False})
        users_give = []
        for temp in users:
            users_give.append(temp)
        return render_template('rank.html', ranker = users_give, user = user)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')

@rank_bp.route('/red', methods=['POST']) # 'GET'
def red():
    token = request.cookies.get('refresh_token')
    if token is not None :
        users = list(db.users.find({'classroom':'레드반'}, {'_id' : False}).sort('total', -1))
        user = db.users.find_one({'token':token}, {'_id' : False})
        users_give = []
        for temp in users:
            users_give.append(temp)
        return render_template('rank.html', ranker = users_give, user = user)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')

@rank_bp.route('/blue', methods=['POST']) # 'GET'
def blue():
    token = request.cookies.get('refresh_token')
    if token is not None :
        users = list(db.users.find({'classroom':'블루반'}, {'_id' : False}).sort('total', -1))
        user = db.users.find_one({'token':token}, {'_id' : False})
        users_give = []
        for temp in users:
            users_give.append(temp)
        return render_template('rank.html', ranker = users_give, user = user)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')

@rank_bp.route('/green', methods=['POST']) # 'GET'
def green():
    token = request.cookies.get('refresh_token')
    if token is not None :
        users = list(db.users.find({'classroom':'그린반'}, {'_id' : False}).sort('total', -1))
        user = db.users.find_one({'token':token}, {'_id' : False})
        users_give = []
        for temp in users:
            users_give.append(temp)
        return render_template('rank.html', ranker = users_give, user = user)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')