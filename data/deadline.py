import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json


class Deadline(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "deadlines"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)

    time = sa.Column(sa.DateTime)
    # author
    
    group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id"))

    tasks = sa.orm.relationship("Task",
                                backref="assignment")
