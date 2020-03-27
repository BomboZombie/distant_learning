from flask_restful import reqparse, Api, abort, Resource
from flask import Blueprint, request, abort

import data as db
from . import manage_sql

user_bp = Blueprint('user_api', __name__)
api = Api(user_bp)

"""
    ВСЕГДА!
если используешь to_dict устанавливай only
для псевдоаттрибутов orm.relationship(), а то рекурсия
< user.to_dict(only=USER_FIELDS) >
"""


# чтобы отличать Teacher от Student используется аргумент usertype
# (s-Student, t-Teacher)
def validate_usertype(usertype):
    if usertype not in ("t", "s"):
        abort(1111, {"error": "Invalid usertype. Options: t, s"})


class UserList(Resource):
    def get(self, usertype):
        validate_usertype(usertype)
        user_class = {"s": db.Student, "t": db.Teacher}.get(usertype)
        return {user_class: manage_sql.display_all_instances(user_class)}


class UserOne(Resource):
    def get(self, usertype, id):
        validate_usertype(usertype)

        user_class = {"s": db.Student, "t": db.Teacher}.get(usertype)
        user = manage_sql.get_instance_by_id(user_class, id)

        return manage_sql.get_object_data(user)


# class TeacherList(UserApi, Resource):
#     def __init__(self):
#         UserApi.__init__(self)
#
#     def get(self):
#         sql = db.create_session()
#         teachers = sql.query(db.Teacher).all()
#         res = []
#         for t in teachers:
#             required_fields = t.to_dict(only=USER_FIELDS)
#             specific_fields = {rel: unwrap_sql_relation(t, rel)
#                                for rel in t.get_related_attrs()}
#             data = {**required_fields, **specific_fields} # их сумма
#             res.append(data)
#         return {"teachers": res}
#
#
# class TeacherApi(UserApi, Resource):
#     def get(self, ):
#         sql = db.create_session()
#         user = sql.query(db.Teacher).get(id)
#         if user is None:
#             abort(404, f"Teacher id {id} does not exist")
#         return user.to_dict(only=USER_FIELDS)

api.add_resource(UserList, '/api/users/<usertype>')
api.add_resource(UserOne, '/api/users/<usertype>/<int:id>')
