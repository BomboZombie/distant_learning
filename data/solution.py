import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json


class Solution(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "solutions"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    created_time = sa.Column(sa.DateTime,
                             default=datetime.datetime.now)
    data = sa.Column(sa.String)
    response = sa.Column(sa.String, nullable=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    task_id = sa.Column(sa.Integer, sa.ForeignKey("tasks.id"))

    def get_related_attrs(self):
        return ("user_id", "task_id")

    def get_non_related_attrs(self):
        return ("id", "created_time", "data", "response",)
