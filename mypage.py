import datetime
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from flask import Flask, render_template,request, make_response, flash, redirect
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token)

mypage_bp = Blueprint('mypage', __name__)

client = MongoClient('localhost', 27017) 
db = client.jranking

@mypage_bp.route("/mypage", methods=['GET'])
def mypage():
    # 1. 내 정보 보여주는 곳
    # DB에서 refresh token 가지고 user id 정보 불러오기
    # 해당 id를 가지고 저장된 모든 데이터를 list로 불러오기
    # 날짜 시작시간 종료시간 데이터 넘겨주기
    
    token = request.cookies.get('refresh_token')
    user = db.users.find_one({'token' : token},{'_id' : False})
    user_id = user['id']
    cursor = db.times.find({'id': user_id},{'_id':False})
    my_data = []
    for document in cursor:
        my_data.append(document)
    
    # 2. 모든 정보 불러와서 평균내기 
    # 2-1. 1위 시간에서 내시간 빼서 보여주기 
    cursor_all = db.users.find({})
    all_data = []
    for document in cursor_all:
        all_data.append(document)
    
    all_data.sort(key=lambda x: x.get('total'),reverse=True)
    number_one = all_data[0]['total'] - user['total']
    return render_template('mypage.html', mydata = my_data, number_one= number_one)

    # 2-2 나의 일일 평균 공부 시간 보여주기
    # 해당 id를 가지고 저장된 모든 데이터를 list로 불러와서,
    # 날짜별로 join 하고 
    # 총 날짜별 length 체크해서 
    # 총 합산 시간 / length 
    # my_data
    
    # 2-3 전체인원 일일 평균 공부시간 보여주기
    # 모든 데이터에서 날짜별로 join 
    # 모든 데이터의 총 합산 시간 / 날짜 length
    # return render_template('mypage.html', mydata = my_data_json, number_one = number_one )

