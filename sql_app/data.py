
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, not_
from sqlalchemy import func
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
    
    def update_class(db: Session, classroom: schemas.Classroom):
        db_class_update = db.query(models.Classroom).filter(
            and_(
                models.Classroom.id == classroom.classid
            )
        ).update({
            'name': classroom.className,
            'grade': classroom.classGrade
        })
        db.commit()
        return db.query(models.Classroom).filter(
            and_(
                models.Classroom.id == classroom.classid
            )
        ).first()
    
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
    
    def get_subject_id(db:Session, id: int):
        return db.query(models.Subject).filter(models.Subject.id == id).all()
    
class StudentMethod:
    def create_student(db: Session, student: schemas.StudentBase):
        db_student = models.Student(name = student.studentName, classId = student.classIn)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    def get_byid(db: Session, studentid: int):
        return db.query(models.Student.id.label("ID"), models.Student.name.label("Name")).filter(models.Student.id == studentid).all()

class SubjectStudentPointMethod:
    def create_point(db: Session, point: schemas.SubjectStudentPointCreate):
        db_point = models.SubjectStudent(
            studentId = point.studentId,
            subjectId = point.subjectId,
            pointFifFirst = point.pointFifFirst,
            pointFifSec = point.pointFifSec,
            pointFirstLast = point.pointFirstLast,
            pointSecLast = point.pointSecLast,
            finnalSum = point.finnalSum
        )
        db.add(db_point)
        db.commit()
        db.refresh(db_point)
        return db_point
    def get_student_point(db: Session, studentSubject: schemas.SubjectStudentPointBase):
        return db.query(models.Student.name.label('Họ và tên'),
                        models.Subject.name.label('Môn học'),
                        models.SubjectStudent.finnalSum.label('Điểm tổng kết')).join(models.Student).join(models.Subject).filter(
            and_(
                models.SubjectStudent.studentId == studentSubject.studentId,
                models.SubjectStudent.subjectId == studentSubject.subjectId
            )
        ).all()
    def get_point_subjectid(db:Session, subjectid: int):
            return db.query(models.Student.name.label('Họ và tên'),
                    models.Classroom.name.label('Lớp'),
                    models.Subject.name.label('Môn học'),
                    models.SubjectStudent.pointFifFirst.label('Điểm 15p lần 1'),
                    models.SubjectStudent.pointFifSec.label('Điểm 15p lần 2'),
                    models.SubjectStudent.pointFirstLast.label('Điểm cuối kỳ 1'),
                    models.SubjectStudent.pointSecLast.label('Điểm cuối kỳ 2'),
                    models.SubjectStudent.finnalSum.label('Điểm tổng kết')).select_from(models.Student).join(models.Classroom).join(models.SubjectStudent).join(models.Subject).filter(
        and_(
            models.SubjectStudent.subjectId == subjectid
        )
    ).all()
            
    def update_point(db: Session, point: schemas.SubjectStudentPointCreate):
        db_point_update = db.query(models.SubjectStudent).filter(
            and_(
                models.SubjectStudent.studentId == point.studentId,
                models.SubjectStudent.subjectId == point.subjectId
            )
        ).update({
            "pointFifFirst": point.pointFifFirst,
            "pointFifSec" : point.pointFifSec,
            "pointFirstLast" : point.pointFirstLast,
            "pointSecLast" : point.pointSecLast,
            "finnalSum" : point.finnalSum
        })
        db.commit()
        return db.query(models.SubjectStudent).filter(
            and_(
                models.SubjectStudent.studentId == point.studentId,
                models.SubjectStudent.subjectId == point.subjectId
            )
        ).first()
        
class SubjectAndStudentMethod:
    def get_all_student(db: Session, studentid: Union[int, None]):
        return db.query(models.Student.name.label('Họ và tên'),
                        models.Subject.name.label('Môn học'),
                        models.SubjectStudent.finnalSum.label('Điểm tổng kết')).join(models.Student).join(models.Subject).filter(models.Student.id == studentid).all()
    
    def get_all_student_all(db: Session):
        return db.query(models.Student.name.label('Họ và tên'),
                        models.Subject.name.label('Môn học'),
                        models.SubjectStudent.finnalSum.label('Điểm tổng kết')).join(models.Student).join(models.Subject).all()     

class ClassAndStudentAndPointMethod:
    def get_all_point(db: Session, classSubject: schemas.ClassAndSubject):
        return db.query(
            models.Student.name.label('Họ và tên'),
            models.Subject.name.label('Môn'),
            models.Classroom.grade.label('Khối'),
            models.SubjectStudent.finnalSum.label('Điểm tổng kết')
            ).select_from(models.Student).join(models.Classroom).join(models.SubjectStudent).join(models.Subject).filter(
                and_(
                    models.Classroom.grade == classSubject.grade,
                    models.SubjectStudent.subjectId == classSubject.subjectid   
                )
            ).all()
    def find_student_point(db: Session, studentInfor: schemas.StudentFind):
        return db.query(
            models.Student.name.label('Họ và tên'),
            models.Classroom.name.label('Lớp'),
            models.Subject.name.label('Môn'),
            models.Classroom.grade.label('Khối'),                        
            models.SubjectStudent.pointFifFirst.label('Điểm 15p lần 1'),
            models.SubjectStudent.pointFifSec.label('Điểm 15p lần 2'),
            models.SubjectStudent.pointFirstLast.label('Điểm cuối kỳ 1'),
            models.SubjectStudent.pointSecLast.label('Điểm cuối kỳ 2'),
            models.SubjectStudent.finnalSum.label('Điểm tổng kết')
            ).select_from(models.Student).join(models.Classroom).join(models.SubjectStudent).join(models.Subject).filter(
                or_(
                    models.Student.id == studentInfor.studentid,
                    models.Student.name == studentInfor.studentName,
                    models.SubjectStudent.pointFifFirst == studentInfor.studentFifFirst,
                    models.SubjectStudent.pointFifSec == studentInfor.studentFifSec,
                    models.SubjectStudent.pointFirstLast == studentInfor.studentFirstLast,
                    models.SubjectStudent.pointSecLast == studentInfor.studentSecLast,
                    models.SubjectStudent.finnalSum == studentInfor.studentFinal
                )
            ).all()
    
class StudentWithIncreasingScoresMethod:
    def get_list(db: Session):
        return db.query(models.Student.name.label('Họ và tên'),
                        models.Subject.name.label('Môn học'),
                        models.SubjectStudent.pointFifFirst.label('Điểm 15p lần 1'),
                        models.SubjectStudent.pointFifSec.label('Điểm 15p lần 2'),
                        models.SubjectStudent.pointFirstLast.label('Điểm 15p lần 3'),
                        models.SubjectStudent.pointSecLast.label('Điểm cuối kỳ 2'),
                        models.SubjectStudent.finnalSum.label('Điểm tổng kết')).filter(and_(
                                                            models.SubjectStudent.pointFifFirst <= models.SubjectStudent.pointFifSec,
                                                            models.SubjectStudent.pointFifSec <= models.SubjectStudent.pointFirstLast,
                                                            models.SubjectStudent.pointFirstLast <= models.SubjectStudent.pointSecLast
                                                        )).join(models.Student).join(models.Subject).order_by(models.Student.id, models.Subject.id).all()

class ClassAndSubjectMethod:
    def get_list(gradeSubject: schemas.ClassAndSubject, db: Session):
        if gradeSubject.grade in (10, 11, 12):
            return db.query(models.Classroom.name.label('Tên lớp'),
                            func.avg(models.SubjectStudent.finnalSum).label('Điểm trung bình'),
                            models.Subject.name.label('Môn học')
                        ).filter(models.Classroom.id == models.Student.classId
                        ).filter(models.Student.id == models.SubjectStudent.studentId
                        ).filter(and_(
                                    models.SubjectStudent.subjectId == models.Subject.id,
                                    models.Classroom.grade == gradeSubject.grade,
                                    models.Subject.id == gradeSubject.subjectid
                                )).group_by(models.Classroom.name).all()
        return db.query(models.Classroom.name.label('Tên lớp'),
                            func.avg(models.SubjectStudent.finnalSum).label('Điểm trung bình'),
                            models.Subject.name.label('Môn học')
                        ).filter(models.Classroom.id == models.Student.classId
                        ).filter(models.Student.id == models.SubjectStudent.studentId
                        ).filter(and_(
                                    models.SubjectStudent.subjectId == models.Subject.id,
                                    models.Subject.id == gradeSubject.subjectid
                                )).group_by(models.Classroom.name).all()
    
class OnlyScoreMethod:
    def get_list(db: Session):
        return db.query(models.Student.name.label('Họ và tên'),
                        func.avg(models.SubjectStudent.finnalSum).label('Điểm tổng kết')
                        ).filter(models.Student.id == models.SubjectStudent.studentId).group_by(models.Student.id).order_by(func.avg(models.SubjectStudent.finnalSum).desc()).all()
    
class GradePointMethod:
    def get_SubjectPointfromClass( db: Session, classSubject: schemas.ClassPoint):
        return db.query(
            models.Subject.name.label('Môn học'),
            models.Classroom.name.label('Lớp'),
            models.SubjectStudent.finnalSum.label('Điểm tổng kết')
            ).select_from(models.Student).join(models.Classroom).join(models.SubjectStudent).join(models.Subject).filter(
                and_(
                    models.Student.classId == classSubject.classid,
                    models.SubjectStudent.subjectId == classSubject.subjectid   
                )
            ).all()

class GetStudentInClass:
    def getStuIn4(classID: int, db: Session):
        return db.query(models.Student).join(models.Classroom).filter(models.Classroom.id == classID).all()
    
