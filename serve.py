import data as db
import datetime
from api import manage_sql

groups = [
    {
        "name": "подготовка к егэ по русскому",
        "teachers": [1, 2],
        "students": [2, 3, 4]
    },
    {
        "name": "олимпиадная физика",
        "teachers": [3],
        "students": [1, 3, 4]
    }
]

students = [
    {
        "name": "Ivan",
        "surname": "Vanko",
        "about": "uchenik 11 klassa",
        "email": "vanya12@g.com",
        "password": "vanya12@g.com"
    },
    {
        "name": "Ridley",
        "surname": "Scott",
        "email": "scott_chief@mars.org",
        "about": "uchenik 11C klassa",
        "password": "scott_chief@mars.org"
    },
    {
        "name": "Lusha",
        "surname": "Potsev",
        "email": "why6mail@mars.org",
        "about": "uchenik 11 klassa",
        "password": "why6mail@mars.org"
    },
    {
        "name": "Andrew",
        "surname": "Dotson",
        "email": "misterdotsonphys@mars.org",
        "about": "uchenik 10 klassa",
        "password": "misterdotsonphys@mars.org"
    },
]

teachers = [
    {
        "name": "Anton",
        "surname": "Huslin",
        "email": "bumblebee@mars.org",
        "password": "bumblebee@mars.org",
        "about": "uchitel zhizni",
        "tasks": [1]
    },
    {
        "name": "John",
        "surname": "Doe",
        "email": "jdoe@mail.ru",
        "password": "jdoe@mail.ru",
        "about": "some random about",
        "tasks": [2]
    },
    {
        "name": "Vasya",
        "surname": "Pupkin",
        "email": "pupok@ya.org",
        "password": "pupok@ya.org",
        "about": "kak ya suda popal?",
        "tasks": [3, 4, 5]
    }
]

tasks = [
    {
        "name": "russki nuzhen",
        "data": "data russki nuzhen"
    },
    {
        "name": "ege na 100",
        "data": "data ege na 100"
    },
    {
        "name": "mehanica",
        "data": "data mehanica"
    },
    {
        "name": "termuha",
        "data": "data termuha"
    },
    {
        "name": "cepi",
        "data": "data cepi"
    }
]

deadlines = [
    {
        "time": datetime.datetime.now() + datetime.timedelta(days=2),
        "group": 1,
        "tasks": [1, 2]
    },
    {
        "time": datetime.datetime.now() + datetime.timedelta(days=3),
        "group": 2,
        "tasks": [3, 4]
    },
    {
        "time": datetime.datetime.now() + datetime.timedelta(days=4),
        "group": 1,
        "tasks": [5]
    },
]


def recreate_db():
    sql = db.create_session()

    for t in teachers:
        teacher = db.Teacher(name=t['name'],
                             surname=t['surname'],
                             email=t['email'],
                             about=t['about'])
        teacher.set_password(t['password'])
        sql.add(teacher)
        for task_id in t['tasks']:
            teacher.tasks.append(db.Task(name=tasks[task_id - 1]["name"],
                                         data=tasks[task_id - 1]["data"]))
    sql.commit()
    sql.close()
    sql = db.create_session()

    for s in students:
        student = db.Student(name=s['name'],
                             surname=s['surname'],
                             email=s['email'],
                             about=s['about'])
        student.set_password(s['password'])
        sql.add(student)
    sql.commit()
    sql.close()
    sql = db.create_session()

    for g in groups:
        group = db.Group(name=g["name"])
        for student_id in g["students"]:
            student = sql.query(db.Student).get(student_id)
            student.groups.append(group)
        for teacher_id in g["teachers"]:
            teacher = sql.query(db.Teacher).get(teacher_id)
            teacher.groups.append(group)
    sql.commit()
    sql.close()
    sql = db.create_session()

    for d in deadlines:
        deadline = db.Deadline(time=d["time"])
        deadline.group = sql.query(db.Group).get(d['group'])
        for task_id in d["tasks"]:
            task = sql.query(db.Task).get(task_id)
            task.deadlines.append(deadline)
    sql.commit()
    sql.close()
