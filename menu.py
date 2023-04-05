from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from flask import Flask, render_template,request, make_response, flash, redirect
from datetime import datetime
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token)

menu_bp = Blueprint('menu', __name__)

@menu_bp.route("/studybutton", methods=['POST', 'GET'])
def studymenu():
    token = request.cookies.get('access_token')
    starttime = datetime.now()
    date = starttime.date()
    starttime = starttime.time().replace(microsecond=0)
    if token is not None :
        return render_template('date.html', date = date, starttime = starttime)
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')
    
@menu_bp.route("/rankbutton", methods=['POST'])
def rankmenu():
    token = request.cookies.get('access_token')
    if token is not None :
        return render_template('rank.html')
    else :
        flash("로그인 정보가 없습니다.")
        return render_template('index.html')