import os
import json
from datetime import timedelta
from flask import *

from forms import *
from data import *

from flask_login import LoginManager, login_required, login_user, logout_user

import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '25=+HSvs2w@&FUkbq-GsqZ4Qe!?ST@KVfrL_T_V!@55BrFtZK*?RMPHDA2DTmwada4&zc*ba4EYYkv#JHe#gSXgUjP&@W$kXyGPTB4ZMvzFbKwxkQ7$CyM?B6aZQ&wFbrERdw#H%JqGE-CX4AdJ4@y!%@^feVx4uG4DCT$45=TxwGed-X5QGda*jqBYUt?mAZ7SC?nbKF$37TWrEAu#P*$?nD5C_wEeFY4n2%5-8hsLS@=dzanQ4uKzawU-Zw4tf'
app.permanent_session_lifetime = timedelta(days=30)  # default


if __name__ == '__main__':
    db_session.global_init("lib/distant_learning.db")

    db = db_session.create_session()

    # g = Group(name="test_group")
    # db.add(g)
    # db.commit()
    # 
    # t = Teacher(name="John",
    #             surname="Doe",
    #             email="jdoe@mail.ru")
    # g.teachers.append(t)
    # db.add(t)
    # db.commit()
    # 
    # s = Student(name="Steve",
    #             surname="Smith",
    #             email="ss_boi@mail.ru")
    # s.groups.append(g)
    # db.add(s)
    # db.commit()

    g = db.query(Group).all()[0]
    print([t for t in g.teachers])
    print([s for s in g.students])

    app.run(port="8080", host='127.0.0.1')
