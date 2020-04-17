import data as db
import datetime
import manage_sql

groups = [
    {
        "name": "подготовка к егэ по русскому",
        "teachers": [1, 2, 3],
        "students": [4, 5, 7]
    },
    {
        "name": "олимпиадная физика",
        "teachers": [3, 7],
        "students": [4, 5, 6]
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
    },
    {
        "name": "ege na 100",
    },
    {
        "name": "mehanica",
    },
    {
        "name": "termuha",
    },
    {
        "name": "cepi",
    }
]

deadlines = [
    {
        "name": "Russki",
        "time": datetime.datetime.now() + datetime.timedelta(days=2),
        "group": 1,
    },
    {
        "name": "PHYS",
        "time": datetime.datetime.now() + datetime.timedelta(days=3),
        "group": 2,
    },
    {
        "name": "more_phys",
        "time": datetime.datetime.now() + datetime.timedelta(days=4),
        "group": 1,
    },
]


def recreate_db():
    sql = db.create_session()

    for t in teachers:
        teacher = db.User(name=t['name'],
                         surname=t['surname'],
                         email=t['email'],
                         about=t['about'])
        teacher.set_password(t['password'])
        for task_id in t['tasks']:
            teacher.tasks.append(db.Task(name=tasks[task_id - 1]["name"]))
            sql.add(teacher)
    sql.commit()
    sql.close()
    sql = db.create_session()

    for s in students:
        student = db.User(name=s['name'],
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
            student = sql.query(db.User).get(student_id)
            student.student_groups.append(group)
        for teacher_id in g["teachers"]:
            teacher = sql.query(db.User).get(teacher_id)
            teacher.teacher_groups.append(group)
    sql.commit()
    sql.close()
    sql = db.create_session()

    for d in deadlines:
        deadline = db.Deadline(time=d["time"], name=d["name"])
        user = sql.query(db.User).get(1)
        deadline.user = user
        deadline.group = sql.query(db.Group).get(d['group'])
    sql.commit()
    sql.close()
