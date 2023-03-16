from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, REAL
from sqlalchemy.orm import relationship
from database import Base

class Classroom(Base):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String(10), nullable=False)
    grade = Column(Integer, index=True, nullable=False)
    
    students = relationship("Student", back_populates="classIn")
    
class Subject(Base):
    __tablename__ = "subject"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String(50), nullable=False)
    
    points = relationship("SubjectStudent", back_populates="subjectPoint")
    
class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String(50), index=True, nullable=False)
    classId = Column(Integer, ForeignKey("class.id"), nullable=False)
    
    classIn = relationship("Classroom", back_populates="students")
    points = relationship("SubjectStudent", back_populates="studentPoint")

class SubjectStudent(Base):
    __tablename__ = "subjectStudent"
    
    studentId = Column(Integer, ForeignKey("student.id"), primary_key=True, index=True, nullable=False)
    subjectId = Column(Integer, ForeignKey("subject.id"), primary_key=True, index= True, nullable=False)
    pointFifFirst = Column(REAL, index=True, nullable=False)
    pointFifSec = Column(REAL, index=True, nullable=False)
    pointFirstLast = Column(REAL, index=True, nullable=False)
    pointSecLast = Column(REAL, index=True, nullable=False)
    finnalSum = Column(REAL, index=True, nullable=False)
    
    studentPoint = relationship("Student", back_populates="points")
    subjectPoint = relationship("Subject", back_populates="points")

