from pymongo import MongoClient
from datetime import timedelta
from flask_cors import CORS
import hashlib
from flask import Flask, render_template, jsonify, url_for,request, make_response, flash, redirect
from flask_jwt_extended import (
    JWTManager, create_access_token,  
    create_refresh_token, jwt_required, get_jwt_identity,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)

app = Flask(__name__)
app.secret_key = "green-eight"
CORS(app, supports_credentials=True)

client = MongoClient('localhost', 27017) 
db = client.jungle

# app.config['BASE_URL'] = 'http://127.0.0.1:5000'
# app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
# app.config["JWT_SECRET_KEY"] = "green-eight" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_CSRF_IN_COOKIES"] = True
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

        # print(access_token)
        # print("--------------")
        # print(refresh_token)
        # # 쿠키에 access token 저장하기
        # #
        # result = make_response({'login': True})
        # set_access_cookies(result, access_token)
        # set_refresh_cookies(result, refresh_token)

        # DB에 refresh token 저장하기
        db.users.update_one({'id' : id},{'$set': {'token': refresh_token}})

        response = make_response(render_template('menu.html'))
        # response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie('access_token', value=access_token)
        return response

@app.route("/menu", methods=['GET'])
def menu():
    token = request.cookies.get('access_token')
    if token is not None :
        return render_template('date.html')
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')

# @app.route('/refresh', methods=['POST'])
# @jwt_required()
# def refresh():
#     current_user = get_jwt_identity()
#     ret = {
#         'access_token': create_access_token(identity=current_user)
#     }
#     return jsonify(ret), 200

@app.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.delete_cookie('access_token')

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