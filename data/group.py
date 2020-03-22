import sqlalchemy as sa
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin  # to-json

student_group = sa.Table('students_to_groups',
                         SqlAlchemyBase.metadata,
                         sa.Column('student',
                                   sa.Integer,
                                   sa.ForeignKey('students.id'), 
                                   primary_key=True),
                         sa.Column('group',
                                   sa.Integer,
                                   sa.ForeignKey('groups.id'), 
                                   primary_key=True)
                         )
teacher_group = sa.Table('teachers_to_groups',
                         SqlAlchemyBase.metadata,
                         sa.Column('teacher',
                                   sa.Integer,
                                   sa.ForeignKey('teachers.id')),
                         sa.Column('group',
                                   sa.Integer,
                                   sa.ForeignKey('groups.id'))
                         )


class Group(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "groups"

    id = sa.Column(sa.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = sa.Column(sa.String)

    # assignments = sa.relationship()
    teachers = sa.orm.relationship("Teacher",
                                   secondary="teachers_to_groups",
                                   backref="groups", 
                                   lazy="dynamic")
    students = sa.orm.relationship("Student",
                                   secondary="students_to_groups",
                                   backref="groups", 
                                   lazy="dynamic")
