import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json


class Problem(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "problems"
    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    text = sa.Column(sa.String)
    answer = sa.Column(sa.String)

    task_id = sa.Column(sa.Integer, sa.ForeignKey("tasks.id"))
