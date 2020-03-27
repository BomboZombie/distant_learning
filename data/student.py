import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from .user import User


class Student(User, SqlAlchemyBase):
    __tablename__ = 'students'

    solutions = sa.orm.relationship("Solution",
                                    backref="student")

    def get_related_attrs(self):
        return ("solutions", )
