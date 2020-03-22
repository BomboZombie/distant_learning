import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json


class Assignment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "assignments"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)
    deadline = sa.Column(sa.DateTime)
    group = sa.orm.relationship("Group")
    tasks = sa.orm.relationship("Task",
                                back_populates="assignment")
