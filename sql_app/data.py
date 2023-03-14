
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, not_
from typing import Union
import sql_app.models as models
import sql_app.schemas as schemas

class ClassroomMethod:
    def create_class(db: Session, classroom: schemas.ClassBase):
        db_classroom = models.Classroom(name = classroom.className, grade = classroom.classGrade)
        db.add(db_classroom)
        db.commit()
        db.refresh(db_classroom)
        return db_classroom
    
    def get_class(db:Session, id: Union[str, None] = None, name: Union[str, None] = None, grade: Union[int, None] = None ):
        return db.query(models.Classroom).filter(
            or_(
                models.Classroom.id == id, 
                models.Classroom.name == name, 
                models.Classroom.grade == grade   
            )
        ).all()
    
    def get_all(db:Session):
        return db.query(models.Classroom).all()

class SubjectMethod:
    def create_subject(db: Session, subject : schemas.SubjectBase):
        db_subject = models.Subject(name = subject.subjectName)
        db.add(db_subject)
        db.commit()
        db.refresh(db_subject)
        return subject
    def get_all(db:Session):
        return db.query(models.Subject).all()
    
class StudentMethod:
    def create_student(db: Session, student: schemas.StudentBase):
        db_student = models.Student(name = student.studentName, classId = student.classIn)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student

class SubjectStudentPointMethod:
    def create_point(db: Session, point: schemas.SubjectStudentPointCreate):
        db_point = models.SubjectStudent( studentId = point.studentId, subjectId = point.subjectId, point = point.point)
        db.add(db_point)
        db.commit()
        db.refresh(db_point)
        return db_point
        
class SubjectAndStudentMethod:
    def get_all_student(db: Session, studentid: Union[int, None], studentname: Union[str, None]):
        return db.query(models.Student.name.label('Họ và tên'),
                        models.Subject.name.label('Môn học'),
                        models.SubjectStudent.point.label('Điểm')).join(models.Student).join(models.Subject).filter( 
            or_(
                models.Student.id == studentid,
                models.Student.name == studentname
            )).all()
class SubjectPointMethod:
    def get_student_point(db: Session, studentid: Union[int, None]):
        return db.query(models.Student.name.label('Họ và tên'),
                        models.Subject.name.label('Môn học'),
                        models.SubjectStudent.point.label('Điểm')).join(models.Student).join(models.Subject).filter( 
            or_(
                models.Student.id == studentid,
                models.Student.name == studentname,
                models.Subject.id == subjectid
            )).all()
