import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json


class Deadline(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "deadlines"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = sa.Column(sa.String)
    time = sa.Column(sa.DateTime)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id"))
    task_id = sa.Column(sa.Integer, sa.ForeignKey("tasks.id"))

    solutions = sa.orm.relationship("Solution",
                                    backref="deadline",
                                    lazy="subquery")

    def get_non_related_attrs(self):
        return ("id", "name", "time", "group_id", "user_id", "task_id")

    def get_related_attrs(self):
        return ("tasks", )
