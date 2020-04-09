import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json

deadline_task = sa.Table('deadlines_to_tasks',
                         SqlAlchemyBase.metadata,
                         sa.Column('task',
                                   sa.Integer,
                                   sa.ForeignKey('tasks.id'),
                                   primary_key=True),
                         sa.Column('deadline',
                                   sa.Integer,
                                   sa.ForeignKey('deadlines.id'),
                                   primary_key=True)
                         )


class Deadline(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "deadlines"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    time = sa.Column(sa.DateTime)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id"))

    tasks = sa.orm.relationship("Task",
                                backref="deadlines",
                                secondary="deadlines_to_tasks")

    def get_non_related_attrs(self):
        return ("id", "time", "group_id")

    def get_related_attrs(self):
        return ("tasks", )
