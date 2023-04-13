from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import json
from flask import Flask, render_template,request, make_response, flash, redirect
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity)

rank_bp = Blueprint('rank', __name__)

client = MongoClient('localhost',27017)
db = client.jungle


@rank_bp.route('/rank', methods=['POST', 'GET'])
@jwt_required()
def rank():
    id = get_jwt_identity()
    if id is not None :
        users = list(db.users.find({}, {'_id' : False}).sort('total', -1))
        user = db.users.find_one({'id':id}, {'_id' : False})
        cnt = 0
        for i in users:
            cnt += 1
            if user['id'] == i['id']:
                break
        users_give = []
        newcnt = 0
        for temp in users:
            users_give.append(temp)
            newcnt += 1
            if newcnt == 5:
                break
        return render_template('rank.html', ranker = users_give, user = user, rank = cnt)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')

@rank_bp.route('/rank/red', methods=['POST', 'GET'])
@jwt_required()
def red():
    id = get_jwt_identity()
    if id is not None :
        allusers = list(db.users.find({}, {'_id' : False}).sort('total', -1))
        users = list(db.users.find({'classroom':'레드반'}, {'_id' : False}).sort('total', -1))
        user = db.users.find_one({'id':id}, {'_id' : False})
        cnt = 0
        for i in allusers:
            cnt += 1
            if user['id'] == i['id']:
                break
        users_give = []
        newcnt = 0
        for temp in users:
            users_give.append(temp)
            newcnt += 1
            if newcnt == 5:
                break
        return render_template('rank.html', ranker = users_give, user = user, rank = cnt)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')

@rank_bp.route('/rank/blue', methods=['POST', 'GET'])
@jwt_required()
def blue():
    id = get_jwt_identity()
    if id is not None :
        allusers = list(db.users.find({}, {'_id' : False}).sort('total', -1))
        users = list(db.users.find({'classroom':'블루반'}, {'_id' : False}).sort('total', -1))
        user = db.users.find_one({'id':id}, {'_id' : False})
        cnt = 0
        for i in allusers:
            cnt += 1
            if user['id'] == i['id']:
                break
        users_give = []
        newcnt = 0
        for temp in users:
            users_give.append(temp)
            newcnt += 1
            if newcnt == 5:
                break
        return render_template('rank.html', ranker = users_give, user = user, rank = cnt)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')

@rank_bp.route('/rank/green', methods=['POST', 'GET'])
@jwt_required()
def green():
    allusers = list(db.users.find({}, {'_id' : False}).sort('total', -1))
    id = get_jwt_identity()
    if id is not None :
        users = list(db.users.find({'classroom':'그린반'}, {'_id' : False}).sort('total', -1))
        user = db.users.find_one({'id':id}, {'_id' : False})
        cnt = 0
        for i in allusers:
            cnt += 1
            if user['id'] == i['id']:
                break
        users_give = []
        newcnt = 0
        for temp in users:
            users_give.append(temp)
            newcnt += 1
            if newcnt == 5:
                break
        return render_template('rank.html', ranker = users_give, user = user, rank = cnt)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')