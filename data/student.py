import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from .user import User


class Student(User, SqlAlchemyBase):
    __tablename__ = 'students'
    
    learning_status = sa.Column(sa.String, nullable=True)

    solutions = sa.orm.relationship("Solution",
                                    backref="student")