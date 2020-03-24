import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from .user import User


class Teacher(User, SqlAlchemyBase):
    __tablename__ = "teachers"

    # subjects

    tasks = sa.orm.relationship("Task",
                                backref="teacher",
                                lazy="dynamic")

    def __repr__(self):
        return f"{self.id} {self.full_name}"
