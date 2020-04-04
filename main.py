import os
import json
import datetime
from flask import *

from flask_login import LoginManager, login_required, login_user, logout_user, current_user

import requests

import forms
import data as db

import api
from api import manage_sql

app = Flask(__name__)
app.config['SECRET_KEY'] = '25=+HSvs2w@&FUkbq-GsqZ4Qe!?ST@KVfrL_T_V!@55BrFtZK*?RMPHDA2DTmwada4&zc*ba4EYYkv#JHe#gSXgUjP&@W$kXyGPTB4ZMvzFbKwxkQ7$CyM?B6aZQ&wFbrERdw#H%JqGE-CX4AdJ4@y!%@^feVx4uG4DCT$45=TxwGed-X5QGda*jqBYUt?mAZ7SC?nbKF$37TWrEAu#P*$?nD5C_wEeFY4n2%5-8hsLS@=dzanQ4uKzawU-Zw4tf'
app.permanent_session_lifetime = datetime.timedelta(days=30)  # default

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(api.user_bp)


@login_manager.user_loader
def load_user(user_id):
    sql = db.create_session()
    return sql.query(db.User).get(user_id)


@app.route("/register", methods=["GET", "POST"])
def register():
    return "<h1>REGISTER</h1>"


@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        sql = db.create_session()
        user = sql.query(db.User).filter(db.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def home():
    if not current_user.is_authenticated:
        return redirect("/login")
    if request.method == "GET":
        student_groups = manage_sql.get_related_objects(current_user, "student_groups")
        teacher_groups = manage_sql.get_related_objects(current_user, "teacher_groups")
        groups = {"student": student_groups, "teacher": teacher_groups}

        current_group_id = session.get("current_group_id")
        if current_group_id is not None:
            current_group = manage_sql.get_one_instance(db.Group, current_group_id)
            teachers = [manage_sql.get_one_instance(db.User, id) for id in current_group["teachers"]]
            students = [manage_sql.get_one_instance(db.User, id) for id in current_group["students"]]
            return render_template("index.html", groups=groups, teachers=teachers, students=students, group=current_group)
        return render_template("index.html", groups=groups, teachers=None, students=None, group=None)

    if request.method == "POST":
        action, id = list(request.form)[0].split("_")
        if action == "loadgroup":
            session["current_group_id"] = int(id)
            return redirect("/")
        elif action == "edit":
            return redirect(f"edit/{id}")
        return redirect("/")


@app.route("/usertasks", methods=["GET", "POST"])
def user_tasks():
    tasks = manage_sql.get_related_objects(current_user, "tasks")
    return render_template("usertasks.html", tasks=tasks)


@app.route("/task/<int:id>", methods=["GET", "POST"])
def manage_task():
    pass


@app.route("/usergroups", methods=["GET", "POST"])
def user_groups():
    groups = manage_sql.get_related_objects(current_user, "teacher_groups")
    return render_template("usergroups.html", groups=groups)


@app.route("/newgroup", methods=["GET"])
def new_group():
    sql = db.create_session()
    new_group = db.Group()
    new_group_id = new_group.id
    sql.add(new_group)
    sql.commit()
    return redirect(f"/group/{new_group_id}")


@app.route("/group/<int:id>", methods=["GET", "POST"])
def manage_group():
    form = forms.GroupForm()




if __name__ == '__main__':
    db.global_init("lib/distant_learning.db")
    # import serve
    # serve.recreate_db()
    app.run(port="8080", host='127.0.0.1')
