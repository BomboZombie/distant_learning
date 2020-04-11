import os
import json
import datetime
import re
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


@app.route("/usertasks", methods=["GET"])
def user_tasks():
    tasks = manage_sql.get_related_objects(current_user, "tasks")
    return render_template("usertasks.html", tasks=tasks)


@app.route("/newtask", methods=["GET"])
def new_task():
    sql = db.create_session()
    new_task = db.Task()
    cu = sql.query(db.User).get(current_user.id) # current_user в этой sql сессии

    cu.tasks.append(new_task)
    sql.commit()

    new_task_id = new_task.id

    sql.close()
    return redirect(f"/task/{new_task_id}")


@app.route("/task/<int:id>", methods=["GET", "POST"])
def manage_task(id):
    if request.method == "GET":
        sql = db.create_session()
        task = sql.query(db.Task).get(id)
        task_data = task.to_dict(only=("name", "description"))

        problems = [p.to_dict(only=("id", "text", "answer")) for p in task.problems]
        return render_template("manageTask.html", data=task_data, problems=problems)
    if request.method == "POST":
        print(request.form)
        data = parse_form(request.form)
        print(data)

        sql = db.create_session()
        task = sql.query(db.Task).get(id)

        # change basic
        if data.get("Name") is not None:
            task.name = data.get("Name").strip()
        if data.get("Desc") is not None:
            task.description = re.sub("\\r\\n", "<br/>", data.get("Desc").strip())

        # change answers
        for pid, ans in map(lambda x: (x[0].strip("a"), x[1]),
                            filter(lambda x: x[0].startswith("a"), data.items())):
            problem = sql.query(db.Problem).get(int(pid))
            problem.answer = ans

        # change text
        for pid, text in map(lambda x: (x[0].strip("t"), x[1]),
                            filter(lambda x: x[0].startswith("t"), data.items())):
            problem = sql.query(db.Problem).get(int(pid))
            problem.text = re.sub("\\r\\n", "<br/>", text)

        # delete
        for pid in remove_prefix(data, "d"):
            problem = sql.query(db.Problem).get(int(pid))
            task.problems.remove(problem)

        # add new
        for k, v in filter(lambda x: x[0].startswith("n"), dict(request.form).items()):
            pidx = int(k[2:]) - 1
            if pidx < len(task.problems):
                problem = task.problems[pidx]
            else:
                problem = db.Problem()
                task.problems.append(problem)

            if k.startswith("na"):
                problem.answer = v.strip()
            elif k.startswith("nt"):
                problem.text = v.strip()


        sql.commit()
        sql.close()

        return redirect(f"/task/{id}")


@app.route("/usergroups", methods=["GET"])
def user_groups():
    groups = manage_sql.get_related_objects(current_user, "teacher_groups")
    sql = db.create_session()
    for g in groups:
        dl_ids = g['deadlines'].copy()
        g["deadlines"] = []
        for did in dl_ids:
            manage_sql.get_one_instance(db.Deadline, did)
            dl = sql.query(db.Deadline).get(did)
            dl_data = dl.to_dict(only=("id", "name", "time", "user_id"))

            dl_data["user"] = dl.user.full_name

            g["deadlines"].append(dl_data)

    # import json
    # print(json.dumps({"groups": groups}, ensure_ascii=True, indent=4))
    return render_template("usergroups.html", groups=groups)


@app.route("/newgroup", methods=["GET"])
def new_group():
    sql = db.create_session()
    new_group = db.Group()
    cu = sql.query(db.User).get(current_user.id) # current_user в этой sql сессии

    cu.teacher_group.append(new_group)
    sql.commit()

    new_group_id = new_group.id

    sql.close()
    return redirect(f"/group/{new_group_id}")


@app.route("/group/<int:id>", methods=["GET", "POST"])
def manage_group(id):
    if request.method == "GET":
        sql = db.create_session()
        group = sql.query(db.Group).get(id)
        group_data = manage_sql.get_object_data(group)
        group_data['teachers'] = [sql.query(db.User).get(uid).to_dict(only=("id", "name", "surname", "email")) for uid in group_data['teachers']]
        group_data['students'] = [sql.query(db.User).get(uid).to_dict(only=("id", "name", "surname", "email")) for uid in group_data['students']]
        sql.close()
        return render_template("manageGroup.html", data=group_data)
    if request.method == "POST":
        data = parse_form(request.form)
        sql = db.create_session()
        group = sql.query(db.Group).get(id)
        if data.get("name") is not None:
            group.name = request.form["name"]

        # delete selected
        for uid in remove_prefix(data.keys(), "dt"):
            user = sql.query(db.User).get(int(uid))
            group.teachers.remove(user)

        for uid in remove_prefix(data.keys(), "ds"):
            user = sql.query(db.User).get(int(uid))
            group.students.remove(user)

        sql.commit()

        # add users to group
        errors = {"not_found":[], "intercept": []}
        for _, email in filter(lambda x: x[0].startswith("at"), data.items()):
            user = sql.query(db.User).filter(db.User.email == email).first()
            if user is None:
                errors["not_found"].append(email)
                continue
            if user in group.students:
                errors["intercept"].append(email)
                continue
            if user not in group.teachers:
                group.teachers.append(user)

        for _, email in filter(lambda x: x[0].startswith("as"), data.items()):
            user = sql.query(db.User).filter(db.User.email == email).first()
            if user is None:
                errors["not_found"].append(email)
                continue
            if user in group.teachers:
                errors["intercept"].append(email)
                continue
            if user not in group.students:
                group.students.append(user)

        # flash errors
        err = False
        if len(errors["not_found"]):
            err = True
            flash("Не удалось найти: ")
            for email in errors["not_found"]:
                flash(email)

        if len(errors["intercept"]):
            err = True
            flash(f"Попытка назначить 2 роли: ")
            for email in errors["intercept"]:
                flash(email)

        sql.commit()
        sql.close()
        if err:
            return redirect(f"/group/{id}")
        return redirect("/usergroups")


@app.route("/newDeadline/<int:group_id>", methods=["GET", "POST"])
def new_deadline(group_id):
    sql = db.create_session()

    group = sql.query(db.Group).get(group_id)
    cu = sql.query(db.User).get(current_user.id)

    dl = db.Deadline(user=cu)

    sql.commit()
    dl_id = dl.id
    sql.close()
    return redirect(f"/deadline/{dl_id}")


@app.route("/deadline/<int:id>", methods=["GET", "POST"])
def manage_deadline(id):
    if request.method == "GET":
        sql = db.create_session()
        deadline = sql.query(db.Deadline).get(id)

        dl_data = deadline.to_dict(only=("name", "time"))
        dl_data["tasks"] = [t.to_dict(only=("name", "id")) for t in deadline.tasks]

        g_data = deadline.group.to_dict(only=("name", ))
        return render_template("manageDeadline.html", deadline=dl_data, group=g_data)
    if request.method == "POST":
        data = parse_form(request.form)

        sql = db.create_session()
        deadline = sql.query(db.Deadline).get(id)

        err = False
        for tid in remove_prefix(data.keys(), "dt"):
            task = sql.query(db.Task).get(tid)
            deadline.tasks.remove(task)

        for tid in remove_prefix(data.keys(), "at"):
            task = sql.query(db.Task).get(tid)
            if task not in deadline.tasks:
                deadline.tasks.append(task)

        # меняем запись в базе если внесли изменения
        deadline.name = data.get("name") if data.get("name") else deadline.name
        deadline.time = datetime.datetime.fromisoformat(data.get("time")) if data.get("time") else deadline.time

        sql.commit()
        sql.close()
        if err:
            return redirect(f"/deadline/{id}")
        return redirect("/usergroups")


@app.route("/deadlineSolutions/<int:dl_id>")
def solved_for_deadline(group_id, dl_id):
    pass

# Вспомогательные функции
def remove_prefix(data, prefix):
    return map(lambda x: x.strip(prefix),
               filter(lambda x: x.startswith(prefix), data))

def parse_form(data):
    return {k:v.strip() for k, v in dict(data).items() if v.strip() != ""}


if __name__ == '__main__':
    db.global_init("lib/distant_learning.db")
    # import serve
    # serve.recreate_db()
    app.run(port="8080", host='127.0.0.1')
