from typing import Union
from pydantic import BaseModel

class ClassBase(BaseModel):
    className: str
    classGrade: int
    
class ClassCreate(ClassBase):
    pass

class ClassStudent(ClassBase):
    id: int
    class Config:
        orm_mode = True
            
class SubjectBase(BaseModel):
    subjectName: str
    
class SubjectCreate(SubjectBase):
    pass

class StudentBase(BaseModel):
    studentName: str
    classIn: int

class StudentCreate(StudentBase):
    pass

class SubjectStudentPointBase(BaseModel):
    studentId: int
    subjectId: int

class SubjectStudentPointCreate(SubjectStudentPointBase):
    pointFifFirst: int
    pointFifSec: int
    pointFirstLast: int
    pointSecLast: int
    finnalSum: int
    class Config:
        orm_mode = True

class SujectAll(SubjectBase):
    id: int
    class Config:
        orm_mode = True    
    
class Student(StudentBase):
    id: int
    class Config:
        orm_mode = True

class SubjectStudentPoint(BaseModel):
    studentid : int
    subjectid: int
    class Config:
        orm_mode = True

class SubjectAvgPoint(SubjectStudentPointBase):
    fiftFirstPoints : float
    midtermPoint : float
    fiftSecPoints : float
    lastTermPoint : float

class ClassAndSubject(BaseModel):
    grade: int 
    subjectid: int
    class Config:
        orm_mode = True

class ClassPoint(BaseModel):
    classid: int
    subjectid: int

class StudentFind(BaseModel):
    studentid: Union[int, None] = None
    studentName: Union[str, None] = None
    studentFinal: Union[float, None] = None
    studentFifFirst:Union[float, None] = None
    studentFifSec: Union[float, None] = None
    studentFirstLast: Union[float, None] = None
    studentSecLast: Union[float, None] = None
    
class Classroom(BaseModel):
    className: str
    classGrade: int
    classid: int
    
class ClassID(BaseModel):
    classID: int