from pymongo import MongoClient
from datetime import timedelta
from flask_cors import CORS
import hashlib
import json
from flask import Flask, render_template, jsonify, url_for,request, make_response, flash, redirect
from flask_jwt_extended import (
    JWTManager, create_access_token,  
    create_refresh_token, jwt_required, get_jwt_identity,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)
import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "green-eight"
# CORS(app, supports_credentials=True)

client = MongoClient('localhost', 27017) 
db = client.jungle

app.config["JWT_SECRET_KEY"] = "green-eight"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# app.config['BASE_URL'] = 'http://127.0.0.1:5000'
# app.config["JWT_COOKIE_SECURE"] = True
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
# app.config["JWT_SECRET_KEY"] = "green-eight" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
# app.config["JWT_CSRF_IN_COOKIES"] = True
# app.config['SESSION_TYPE'] = 'filesystem'

jwt = JWTManager(app)

app.config.update(
    DEBUG=True,
    JWT_SECRET_KEY="JUNGLERSSPORTS",
)

@app.route('/')
def home():
    jwtToken = request.cookies.get('access_token')
    if jwtToken is None :
        return render_template('index.html')
    else :
        return render_template('menu.html')
    # access_token = request.cookies.get('access_token')
    # if access_token is None :
    #     return render_template('index.html')
    # else :
    #     response = make_response(render_template('index.html'))
    #     response.set_cookie('access_token', 'YOUR_ACCESS_TOKEN')
    #     response.set_cookie('refresh_token', 'YOUR_REFRESH_TOKEN')
    #     return response

@app.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    password = request.form['password']
    user = db.users.find_one({'id' : id})
    
    if (user == None) or (user['password'] != password) :
        flash('아이디와 패스워드가 일치하지 않습니다.')
        return redirect("http://127.0.0.1:5000/")
    else :
        # DB에 access_token, refresh token 생성하기
        access_token = create_access_token(identity=id)
        refresh_token = create_refresh_token(identity=id)

        # DB에 refresh token 저장하기
        db.users.update_one({'id' : id},{'$set': {'token': refresh_token}})
        response = make_response(render_template('menu.html'))
        response.set_cookie('access_token', value=access_token)
        response.set_cookie('refresh_token', value=refresh_token)
        
        return response
    
@app.route('/signupbutton', methods=['POST'])
def signupbutton():
    return render_template('signup.html')

# 회원가입
@app.route('/signup', methods=['POST'])
def postUser():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        name = request.form['name']
        classroom = request.form['classroom']
        
        # 이름 입력 확인
        if name == '':
            flash("이름을 입력해주세요!")
            return render_template('signup.html')
        
        # id 중복 확인
        temp = list(db.users.find({}))
        for user in temp:
            if id in user['id']:
                flash("중복된 ID입니다!")
                return render_template('signup.html')
        
        # pw 길이 확인
        if len(password) < 8:
            flash("8글자 이상의 비밀번호를 입력해주세요!")
            return render_template('signup.html')
        
        # 반 선택 확인
        if classroom == '---':
            flash("반을 선택해주세요!")
            return render_template('signup.html')
        
        # db에 저장
        db.users.insert_one({'id':id, 'password':password, 'name':name, 'classroom':classroom, 'total':0, 'token':''})
        flash("가입이 완료되었습니다!")
        return render_template('index.html')
    else:
        return render_template('signup.html')

@app.route("/study", methods=['POST'])
def menu():
    token = request.cookies.get('access_token')
    if token is not None :
        return render_template('date.html')
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')

@app.route("/rank", methods=['POST'])
def rank():
    token = request.cookies.get('access_token')
    if token is not None :
        return render_template('rank.html')
        users = list(db.users.find({}).sort({'total': -1}))
        user = list(db.users.find_one({'id':id}))
        return render_template('rank.html', 
                               r1name=users[0]['name'], r1total=users[0]['total'], 
                               r2name=users[1]['name'], r2total=users[1]['total'], 
                               r3name=users[2]['name'], r3total=users[2]['total'], 
                               r4name=users[3]['name'], r4total=users[3]['total'], 
                               r5name=users[4]['name'], r5total=users[4]['total'])
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')
    
@app.route("/logout", methods=['POST'])
def logout():
    token = request.cookies.get('access_token')
    response = make_response(render_template('index.html'))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

@app.route("/mypage", methods=['POST'])
def mypage():
    
    # 1. 내 정보 보여주는 곳
    # DB에서 refresh token 가지고 user id 정보 불러오기
    # 해당 id를 가지고 저장된 모든 데이터를 list로 불러오기
    # 날짜 시작시간 종료시간 데이터 넘겨주기
    token = request.cookies.get('refresh_token')
    my_data_id_only = db.users.find_one({'token' : token}, {'token' : False}, {'_id':False}, {'password':False},{'name':False}, {'classroom':False}, {'total':False})
    my_data = list(db.times.find({'id': my_data_id_only['id']}))
    my_data_json = json.dumps(my_data)
    
    
    # 2. 모든 정보 불러와서 평균내기 
    # 2-1. 1위 시간에서 내시간 빼서 보여주기 
    all_data = list(db.users.find({}))
    all_data.sort(key=lambda x: x.get('total'),reverse=True)
    my_data_all = db.users.find_one({'id' : my_data_id_only['id']})
    number_one = all_data[0]['total'] - my_data_all['total']
    
    # 2-2 나의 일일 평균 공부 시간 보여주기
    # 해당 id를 가지고 저장된 모든 데이터를 list로 불러와서,
    # 날짜별로 join 하고 
    # 총 날짜별 length 체크해서 
    # 총 합산 시간 / length 
    
    # 2-3 전체인원 일일 평균 공부시간 보여주기
    # 모든 데이터에서 날짜별로 join 
    # 모든 데이터의 총 합산 시간 / 날짜 length
    return render_template('home.html', mydata = my_data_json, number_one = number_one )


# 만들어야할 것 
# access 토큰이 만료되었을때, 재발급 받는 방법. 

if __name__ == '__main__':
#    app.secret_key = "green-eight"
#    app.config['SESSION_TYPE'] = 'filesystem'
#    sess.init_app(app)
   app.run('0.0.0.0',port=5000,debug=True)
   
   
   
# @app.route('/refresh', methods=['GET'])
# @jwt_refresh_token_required
# def refresh():
#     current_user = get_jwt_identity()
#     access_token = create_access_token(identity=current_user)
#     return jsonify(access_token=access_token, current_user=current_user)