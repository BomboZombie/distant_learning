import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin  # flask-login

from sqlalchemy_serializer import SerializerMixin  # to-json


class User(UserMixin, SerializerMixin, SqlAlchemyBase):
    __tablename__ = "users"
    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = sa.Column(sa.String)
    surname = sa.Column(sa.String)
    email = sa.Column(sa.String,
                      index=True,
                      unique=True)
    about = sa.Column(sa.String, nullable=True)
    hashed_password = sa.Column(sa.String)

    messages = sa.orm.relationship("Message",
                                   backref="user")
    tasks = sa.orm.relationship("Task",
                                backref="user")
    solutions = sa.orm.relationship("Solution",
                                    backref="student")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @property
    def full_name(self):
        return " ".join([self.name, self.surname])

    def get_non_related_attrs(self):
        return ("id", "name", "surname", "email", "about")

    def get_related_attrs(self):
        return ("solutions",
                "groups", "tasks")
