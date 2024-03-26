from datetime import datetime

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from connect_db import engine

Base = declarative_base()


class StudentGroup(Base):
    __tablename__ = "student_groups"
    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(25), nullable=False)

class Lecturer(Base):
    __tablename__ = "lecturers"
    lecturer_id = Column(Integer, primary_key=True, autoincrement=True)
    lecturer_name = Column(String(255), unique=True, nullable=False)

class Subject(Base):
    __tablename__ = "subjects"
    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(255), nullable=False)
    lecturer_id = Column(Integer, ForeignKey(Lecturer.lecturer_id, onupdate="CASCADE"), nullable=False)
    lecturer = relationship('Lecturer', backref='subjects')
    group_id = Column(Integer, ForeignKey(StudentGroup.group_id, onupdate="CASCADE"), nullable=False)  ##
    group = relationship("StudentGroup", backref="subjects")  ##

class Student(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    student_name = Column(String(255), nullable=False)

    student_group_id = Column(Integer, ForeignKey(StudentGroup.group_id, onupdate="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.subject_id, onupdate="CASCADE"))
    subjects = relationship("Subject", backref='students')
    grades = relationship('Grade', backref='student')
    group = relationship("StudentGroup", backref="student")

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    grade = Column(Float, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    subject = relationship('Subject', backref='grades')


Base.metadata.create_all(engine)