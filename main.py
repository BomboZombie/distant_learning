import os
import json
import datetime
from flask import *

from flask_login import LoginManager, login_required, login_user, logout_user

import requests

from forms import *
import data as db

app = Flask(__name__)
app.config['SECRET_KEY'] = '25=+HSvs2w@&FUkbq-GsqZ4Qe!?ST@KVfrL_T_V!@55BrFtZK*?RMPHDA2DTmwada4&zc*ba4EYYkv#JHe#gSXgUjP&@W$kXyGPTB4ZMvzFbKwxkQ7$CyM?B6aZQ&wFbrERdw#H%JqGE-CX4AdJ4@y!%@^feVx4uG4DCT$45=TxwGed-X5QGda*jqBYUt?mAZ7SC?nbKF$37TWrEAu#P*$?nD5C_wEeFY4n2%5-8hsLS@=dzanQ4uKzawU-Zw4tf'
app.permanent_session_lifetime = datetime.timedelta(days=30)  # default


def recreate_db():
    sql = db.create_session()

    g = db.Group(name="test_group")

    t = db.Teacher(name="John",
                surname="Doe",
                email="jdoe@mail.ru")
    g.teachers.append(t)
    sql.add(t)
    sql.commit()

    s = db.Student(name="Steve",
                surname="Smith",
                email="ss_boi@mail.ru")
    s.groups.append(g)
    sql.add(s)
    sql.commit()


if __name__ == '__main__':
    db.global_init("lib/distant_learning.db")
    sql = db.create_session()
    
    dls = sql.query(db.Group).get(1).deadlines
    for dl in dls:
        print(dl.time)
        for t in dl.tasks:
            print(t.name, t.teacher.name, t.teacher.surname)
    
    # g = sql.query(db.Group).get(1)
    # 
    # task1 = db.Task(
    #     name="TASK1",
    #     teacher_id=1
    # )
    # task2 = db.Task(
    #     name="TASK2",
    #     teacher_id=1
    # )
    # 
    # dl = db.Deadline(
    #     group=g,
    #     time=datetime.datetime.now() + datetime.timedelta(days=2)
    # )
    # dl.tasks.append(task1)
    # dl.tasks.append(task2)
    # 
    # sql.commit()

    app.run(port="8080", host='127.0.0.1')
