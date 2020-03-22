import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from .user import User
        

class Teacher(User, SqlAlchemyBase):
    __tablename__ = "teachers"

    # subjects = sa.Column(sa.ARRAY(sa.String), nullable=True)

    # tasks = sa.orm.relation("Task",
    #                          backref="teacher")
