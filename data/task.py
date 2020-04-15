import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "tasks"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = sa.Column(sa.String, default="Задание Без Названия")
    created_time = sa.Column(sa.DateTime,
                             default=datetime.datetime.now)
    description = sa.Column(sa.String, default="""Описания нет :-( <br/>
                                                  Должно быть вы знаете, что делать""")

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    deadlines = sa.orm.relationship("Deadline",
                                    backref="task",
                                    lazy="subquery")
    problems = sa.orm.relationship("Problem",
                                    backref="task",
                                    lazy="subquery")

    def get_related_attrs(self):
        return None

    def get_non_related_attrs(self):
        return ("id", "name", "created_time", "user_id")
