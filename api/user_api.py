from flask_restful import reqparse, Api, abort, Resource
from flask import Blueprint, request
import data as db

user_bp = Blueprint('user_api', __name__)
api = Api(user_bp)

"""
    ВСЕГДА!
если используешь to_dict устанавливай only
для псевдоаттрибутов orm.relationship(), а то рекурсия
< user.to_dict(only=USER_FIELDS) >
"""
USER_FIELDS = ("id", "name", "surname", "email", "about")

class UserList(Resource):
    """
        чтобы отличать Teacher от Student используется
        аргумент usertype (s-Student, t-Teacher)
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument("usertype", choices=('s', 't'), required=True)
        
        self.reqparse.add_argument("name")
        self.reqparse.add_argument("surname")
        self.reqparse.add_argument("email")
        self.reqparse.add_argument("about")
        self.reqparse.add_argument("hashed_password")

    def get(self):
        usertype = self.reqparse.parse_args().get("usertype")
        sql = db.create_session()
        if usertype == "s":
            users = sql.query(db.Student).all()
        elif usertype == "t":
            users = sql.query(db.Teacher).all()
        return {usertype: [u.to_dict(only=USER_FIELDS) for u in users]}

    def post(self):
        usertype = self.reqparse.parse_args().get("usertype")
        if not request.json:
            return jsonify({'error': 'Empty request'})
        # if any(self.reqparse.get(v) is None for v in [""]):
        #     return jsonify()
        
        sql = db.create_session()
        user = db.User()
        for k, v in self.reqparse:
            setattr(user, k, v)
        sql.add(user)
        

api.add_resource(UserList, '/api/users/s')
