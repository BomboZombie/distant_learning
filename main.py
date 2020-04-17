import os
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
app.permanent_session_lifetime = datetime.timedelta(days=30)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    sql = db.create_session()
    return sql.query(db.User).get(user_id)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        sql = db.create_session()
        if sql.query(db.User).filter(db.User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = db.User(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data
        )
        user.set_password(form.password.data)
        sql.add(user)
        sql.commit()
        return redirect('/login')

    return render_template('register.html', form=form)


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


@app.route("/", methods=["GET"])
def home():
    if not current_user.is_authenticated:
        return redirect("/login")

    sql = db.create_session()

    groups = []
    for g in current_user.student_groups:
        g_data = g.to_dict(only=("name", ))
        g_data['deadlines'] = []
        for dl in g.deadlines:
            dl_data = dl.to_dict(only=("id", "name", "time", "task_id"))

            solution = get_present(dl.solutions, lambda s: s.user_id == current_user.id)
            if dl.time < datetime.datetime.now():
                if solution is not None:
                    dl_data['status'] = {"text": f"Результат: {solution.percentage}",
                                         "show": True}
                else:
                    dl_data['status'] = {"text": "Срок пропущен",
                                         "show": True}
            else:
                if solution is not None:
                    dl_data['status'] = {"text": "Сдано",
                                         "show": False}
                else:
                    dl_data['status'] = {"text": "Не сдано",
                                         "show": False}
            g_data['deadlines'].append(dl_data)

        groups.append(g_data)
    return render_template("index.html", groups=groups)


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
        sql.close()
        return render_template("manageTask.html", data=task_data, problems=problems)
    if request.method == "POST":
        data = parse_form(request.form)

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
            problem.answer = ans.strip()

        # change text
        for pid, text in map(lambda x: (x[0].strip("t"), x[1]),
                            filter(lambda x: x[0].startswith("t"), data.items())):
            problem = sql.query(db.Problem).get(int(pid))
            problem.text = re.sub("\\r\\n", "<br/>", text)

        # delete
        for pid in remove_prefix(data, "d"):
            problem = sql.query(db.Problem).get(int(pid))
            task.problems.remove(problem)
            # sql.delete(problem)

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
                problem.text = re.sub("\\r\\n", "<br/>", v.strip())

        if len(task.problems) == 0:
            flash("В задании нет задач")

        sql.commit()
        sql.close()
        return redirect(f"/task/{id}")

@app.route("/solve/<int:dl_id>", methods=["GET", "POST"])
def solve(dl_id):
    if request.method == "GET":
        sql = db.create_session()
        dl = sql.query(db.Deadline).get(dl_id)
        task = dl.task

        if task is None:
            return render_template("solve.html", problems=[], data=None)

        problems = []
        for p in task.problems:
            p_data = p.to_dict(only=("id", "text"))
            problems.append(p_data)

        data = task.to_dict(only=("description", "name"))
        sql.close()
        return render_template("solve.html", problems=problems, data=data)
    if request.method == "POST":
        sql = db.create_session()
        dl = sql.query(db.Deadline).get(dl_id)
        task = dl.task

        mistakes = []
        for idx, el in enumerate(dict(request.form).items()):
            pid, ans = el[0], el[1]
            problem = sql.query(db.Problem).get(int(pid))
            if ans.strip() != problem.answer:
                mistakes.append(str(idx + 1))
        percentage = int((len(task.problems) - len(mistakes)) / len(task.problems) * 100)

        # если уже решал - перезаписать решение
        solution = get_present(dl.solutions, lambda s: s.user_id == current_user.id)
        if solution is None:
            solution = db.Solution()
            sql.add(solution)

        solution.user_id = current_user.id
        solution.deadline_id = dl.id
        solution.percentage = percentage
        solution.mistakes = ",".join(mistakes)

        sql.commit()
        sql.close()
        return redirect(f"/")


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
    return render_template("usergroups.html", groups=groups)


@app.route("/newgroup", methods=["GET"])
def new_group():
    sql = db.create_session()
    new_group = db.Group()
    cu = sql.query(db.User).get(current_user.id) # current_user в этой sql сессии

    cu.teacher_groups.append(new_group)
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
        if len(errors["not_found"]):
            flash("Не удалось найти: ")
            for email in errors["not_found"]:
                flash(email)

        if len(errors["intercept"]):
            flash(f"Попытка назначить 2 роли: ")
            for email in errors["intercept"]:
                flash(email)

        sql.commit()
        sql.close()
        return redirect(f"/group/{id}")


@app.route("/newDeadline/<int:group_id>", methods=["GET", "POST"])
def new_deadline(group_id):
    sql = db.create_session()

    group = sql.query(db.Group).get(group_id)
    cu = sql.query(db.User).get(current_user.id)

    dl = db.Deadline(user=cu,
                     group=group)

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
        if deadline.task is not None:
            dl_data["task"] = deadline.task.to_dict(only=("name", "id"))

        g_data = deadline.group.to_dict(only=("name", ))
        sql.close()
        return render_template("manageDeadline.html", deadline=dl_data, group=g_data)
    if request.method == "POST":
        data = parse_form(request.form)

        sql = db.create_session()
        deadline = sql.query(db.Deadline).get(id)

        if "delete" in data:
            sql.delete(deadline)
            sql.commit()
            sql.close()
            return redirect("/usergroups")

        for tid in remove_prefix(data.keys(), "at"):
            task = sql.query(db.Task).get(tid)
            deadline.task = task

        # меняем запись в базе если внесли изменения
        deadline.name = data.get("name") if data.get("name") else deadline.name
        deadline.time = datetime.datetime.fromisoformat(data.get("time")) if data.get("time") else deadline.time

        if deadline.task is None:
            flash("Выберите задание")
        if deadline.name is None:
            flash("Придумайте название")
        if deadline.time is None:
            flash("Назначте время")

        sql.commit()
        sql.close()
        return redirect(f"/deadline/{id}")


@app.route("/solutions/<int:dl_id>")
def solutions(dl_id):
    sql = db.create_session()
    dl = sql.query(db.Deadline).get(dl_id)
    sols = []
    for s in dl.solutions:
        data = s.to_dict(only=("percentage", "mistakes"))
        data["user"] = s.user.full_name
        sols.append(data)
    info = dl.to_dict(only=("time", "name"))
    info["task"] = dl.task.name
    sql.close()
    return render_template("solutions.html", solutions=sols, data=info)


@app.route("/correct/<int:task_id>")
def correct(task_id):
    sql = db.create_session()
    task = sql.query(db.Task).get(task_id)
    task_data = task.to_dict(only=("name", "description"))

    problems = [p.to_dict(only=("id", "text", "answer")) for p in task.problems]
    solution = get_present(current_user.solutions, lambda s: s.deadline.task_id == task_id)
    if solution is not None:
        solution = solution.to_dict(only=("percentage", "mistakes"))

    sql.close()
    return render_template("correct.html", data=task_data, problems=problems, solution=solution)


# Вспомогательные функции
def remove_prefix(data, prefix):
    return map(lambda x: x.strip(prefix),
               filter(lambda x: x.startswith(prefix), data))

def parse_form(data):
    return {k:v.strip() for k, v in dict(data).items() if v.strip() != ""}

def get_present(data, func):
    return next(filter(func, data), None)

if __name__ == '__main__':
    db.global_init("lib/distant_learning.db")
    app.run(port="8080", host='127.0.0.1')
