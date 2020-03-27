import os
import json
import datetime
from flask import *

from flask_login import LoginManager, login_required, login_user, logout_user

import requests

import forms
import data as db
import api
from api import manage_sql

app = Flask(__name__)
app.config['SECRET_KEY'] = '25=+HSvs2w@&FUkbq-GsqZ4Qe!?ST@KVfrL_T_V!@55BrFtZK*?RMPHDA2DTmwada4&zc*ba4EYYkv#JHe#gSXgUjP&@W$kXyGPTB4ZMvzFbKwxkQ7$CyM?B6aZQ&wFbrERdw#H%JqGE-CX4AdJ4@y!%@^feVx4uG4DCT$45=TxwGed-X5QGda*jqBYUt?mAZ7SC?nbKF$37TWrEAu#P*$?nD5C_wEeFY4n2%5-8hsLS@=dzanQ4uKzawU-Zw4tf'
app.permanent_session_lifetime = datetime.timedelta(days=30)  # default

app.register_blueprint(api.user_bp)

@app.route("/register", methods=["GET", "POST"])
def register():
    return "<h1>REGISTER</h1>"


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template()


@app.route("/")
def home():
    groups = manage_sql.get_all_instances(db.Group)
    teachers = manage_sql.get_all_instances(db.Teacher)
    students = manage_sql.get_all_instances(db.Student)
    return render_template("index.html", groups=groups, teachers=teachers, students=students)


if __name__ == '__main__':
    db.global_init("lib/distant_learning.db")
    app.run(port="8080", host='127.0.0.1')
