import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin  # flask-login

from sqlalchemy_serializer import SerializerMixin  # to-json


class User(UserMixin, SerializerMixin):
    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = sa.Column(sa.String)
    surname = sa.Column(sa.String)
    email = sa.Column(sa.String,
                      index=True,
                      unique=True)
    # about = string(1000)
    hashed_password = sa.Column(sa.String)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @property
    def full_name(self):
        return " ".join([name, surname])
