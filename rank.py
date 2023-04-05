from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import json
from flask import Flask, render_template,request, make_response, flash, redirect
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token)

rank_bp = Blueprint('rank', __name__)

client = MongoClient('localhost', 27017) 
db = client.jungle


@rank_bp.route("/rank", methods=['POST'])
def rank():
    token = request.cookies.get('refresh_token')
    if token is not None :
        users = list(db.users.find({}).sort({'total': -1}))
        user = list(db.users.find_one({'token':token}))
        users = json.dumps(users)
        user = json.dumps(user)
        return render_template('rank.html', ranker = users, user = user)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')

@rank_bp.route("/rank/red", methods=['GET'])
def red():
    token = request.cookies.get('refresh_token')
    if token is not None :
        users = list(db.users.find({'classroom':'red'}).sort({'total': -1}))
        user = list(db.users.find_one({'token':token}))
        users = json.dumps(users)
        user = json.dumps(user)
        return render_template('rank.html', ranker = users, user = user)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')
    
@rank_bp.route("/rank/blue", methods=['GET'])
def blue():
    token = request.cookies.get('refresh_token')
    if token is not None :
        users = list(db.users.find({'classroom':'blue'}).sort({'total': -1}))
        user = list(db.users.find_one({'token':token}))
        users = json.dumps(users)
        user = json.dumps(user)
        return render_template('rank.html', ranker = users, user = user)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')

@rank_bp.route("/rank/green", methods=['GET'])
def green():
    token = request.cookies.get('refresh_token')
    if token is not None :
        users = list(db.users.find({'classroom':'green'}).sort({'total': -1}))
        user = list(db.users.find_one({'token':token}))
        users = json.dumps(users)
        user = json.dumps(user)
        return render_template('rank.html', ranker = users, user = user)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')