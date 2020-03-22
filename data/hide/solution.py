import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json


class Solution(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "solutions"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = sa.Column(sa.String)
    created_time = sa.Column(sa.DateTime,
                             default=datetime.datetime.now)
    data = sa.Column(sa.JSON)

    student_id = sa.Column(sa.Integer, sa.ForeignKey("students.id"))
    task = sa.orm.relationship("Task")
