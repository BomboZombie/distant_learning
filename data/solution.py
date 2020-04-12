import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json


class Solution(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "solutions"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    persentage = sa.Column(sa.Integer)
    mistakes = sa.Column(sa.String)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    deadline_id = sa.Column(sa.Integer, sa.ForeignKey("deadlines.id"))

    def get_related_attrs(self):
        return ("user_id", "task_id")

    def get_non_related_attrs(self):
        return ("id", "created_time", "data", "response",)
