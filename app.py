from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token,  create_refresh_token
)

app = Flask(__name__)

client = MongoClient('localhost', 27017) 
db = client.jungle

app.config['JWT_SECRET_KEY'] = 'secret-key'

jwt = JWTManager(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    password = request.form['password']

    user = db.jranking.users.find_one({}, {'id' : id,'password' : password})
    
    if user is None :
        return jsonify({'result': 'false', "msg": "Bad username or password"}), 401
        
    # DB에 access_token, refresh token 생성하기
    access_token = create_access_token(identity=id)
    refresh_token = create_refresh_token(identity=id)
    
    # DB에 refresh token 저장하기
    db.jranking.users.update_one({'id' : id},{'$set': {'token': refresh_token}})
    
    return jsonify({'result': 'success', 'access_token': access_token, 'refresh_token':refresh_token}), 200

# @app.route('/refresh', methods=['GET'])
# @jwt_refresh_token_required
# def refresh():
#     current_user = get_jwt_identity()
#     access_token = create_access_token(identity=current_user)
#     return jsonify(access_token=access_token, current_user=current_user)