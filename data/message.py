import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "messages"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)
                   
    created_time = sa.Column(sa.DateTime,
                             default=datetime.datetime.now)
    data = sa.Column(sa.String)
    
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    group_id = sa.Column(sa.Integer, sa.ForeignKey("groups.id"))