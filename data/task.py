import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "tasks"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = sa.Column(sa.String)
    created_time = sa.Column(sa.DateTime,
                             default=datetime.datetime.now)
    data = sa.Column(sa.String())

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    
    solutions = sa.orm.relationship("Solution",
                                    backref="task", 
                                    lazy="dynamic")

    def get_related_attrs(self):
        return ("solutions", )

    def get_non_related_attrs(self):
        return ("id", "name", "created_time", "data", "user_id")
