from fastapi import FastAPI, Depends, FastAPI, HTTPException, Path
from starlette.responses import FileResponse 
from sqlalchemy.orm import Session
from typing import Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sql_app.models as models
import sql_app.schemas as schemas
import sql_app.data as data
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine, get_db
from sql_app.default import initDef 
from fastapi.responses import HTMLResponse
import webbrowser
import os

templates = Jinja2Templates(directory="pages/")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# initDef()

@app.get('/', response_class=HTMLResponse, tags=['Trang chủ'])
def home():
    html_content = '''
    <html>
        <head>
            <title>Welcome BTL Python</title>
            <style>
                h1{
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>Bài tập lớn môn Lập trình Python</h1>
            <br> </br>
            <div>
                <h2>Nhóm gồm 4 thành viên:</h2>
                <ul>
                    <li>A38253 Nguyễn Hoàng Đức Anh</li>
                    <li>A38520 Mai Văn Mạnh</li>
                    <li>A38911 Vũ Tiến Dũng</li>
                    <li>A41174 Hoàng Chí Hiếu</li>
                </ul>
            </div>
            <br> </br>
            <div> 
                <h2>Đề tài: Quản lý điểm học sinh</h2>
                <h3>Phân công công việc:</h3>
                <li>A38253 Nguyễn Hoàng Đức Anh</li>
                <ul>
                    <li> GET:</li>
                    <ul>
                        <li>numpy: </li>
                        <li>pandas: </li>
                    </ul>
                    <li> POST:</li>
                    <ul>
                        <li>numpy: </li>
                        <li>pandas: </li>
                    </ul>
                </ul>
                <li>A38520 Mai Văn Mạnh</li>
                <ul>
                    <li> GET:</li>
                    <ul>
                        <li>numpy: </li>
                        <li>pandas: </li>
                    </ul>
                    <li> POST:</li>
                    <ul>
                        <li>numpy: </li>
                        <li>pandas: </li>
                    </ul>
                </ul>         
                <li>A38911 Vũ Tiến Dũng</li>
                <ul>
                    <li> GET:</li>
                    <ul>
                        <li>numpy: </li>
                        <li>pandas: </li>
                    </ul>
                    <li> POST:</li>
                    <ul>
                        <li>numpy: </li>
                        <li>pandas: </li>
                    </ul>
                </ul>
                <li>A41174 Hoàng Chí Hiếu</li>
                <ul>
                    <li> GET:</li>
                    <ul>
                        <li>numpy: </li>
                        <li>pandas: </li>
                    </ul>
                    <li> POST:</li>
                    <ul>
                        <li>numpy: </li>
                        <li>pandas: </li>
                    </ul>
                </ul>
            </div>

        </body>
    </html>
    '''
    return HTMLResponse(content=html_content, status_code=200)

#region Manh
#pd
@app.get('/subject/DiemCuaMon', 
         tags = ['Điểm của học sinh theo môn'], 
         description= ('Nhập mã học sinh và mã môn để xem được điểm tổng môn đó theo mã học sinh'))
def get_point_subject(
    studentid: Union[int, None] = None, 
    subjectid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if(studentid != None or subjectid !=None):
        studentPoint= data.SubjectStudentPointMethod.get_student_point(db, schemas.SubjectStudentPointBase(studentId=studentid, subjectId=subjectid));
        if np.array(studentPoint).size !=0:
            df = pd.DataFrame.from_dict(studentPoint)
            diem = df['Điểm tổng kết'][0]
            name = df['Họ và tên'][0]
            subject = df['Môn học'][0]
            return {"result": f'Điểm của {name} với môn {subject} là: {diem}'}
        else:
            if np.array(data.StudentMethod.get_byid(db, studentid=studentid)).size == 0:
                raise HTTPException(status_code=404, detail= {
                    "field": "studentid",
                    "errMsg": "Không tồn tại sinh viên"})
            elif np.array(data.SubjectMethod.get_subject_id(db, id= subjectid)).size == 0:
                raise HTTPException(status_code=404, detail= {
                    "field": "subjectid",
                    "errMsg": "Không tồn tại môn học"})
    else: 
        raise HTTPException(status_code=404, detail="Chưa có thông tin nào về học sinh được đưa ra (studentid: int, subjectid: int)")

@app.get('/subject/DiemTongKetCuaHocSinh', 
         tags=['Điểm tổng kết của học sinh'],
         description=('Nhập mã học sinh để có thể xem bảng điểm của học sinh đó'))
def get_student_point_subject(
    studentid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if( studentid != None):
        studentInClass = data.SubjectAndStudentMethod.get_all_student(db, studentid=studentid)
        df = pd.DataFrame.from_dict(studentInClass)
        df['Điểm tổng kết'] = df['Điểm tổng kết'].fillna(0)
        diem = df['Điểm tổng kết'].tolist()
        subject = df['Môn học'].to_list()
        name = df['Họ và tên'][0]
        subject.insert(0, 'Họ và tên')
        diem.insert(0, name)
        dataframe = pd.DataFrame(data = diem, index= subject)
        print(dataframe.T)
        return dataframe
    else: 
        raise HTTPException(status_code=404, detail={
            "field": "studentid",
            "errMsg": "Chưa có thông tin"
        })

#np
@app.get('/subject/Diem', 
         tags= ['Điểm trung bình môn theo lớp'], 
         description= ('Nhập mã lớp và mã môn để có thể xem được điểm trung bình của môn đó theo lớp'))
def get_Diem(
    classid: Union[int, None] = None, 
    subjectid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if(classid != None or subjectid != None):
        ClassPoint = data.GradePointMethod.get_SubjectPointfromClass(db, schemas.ClassPoint(classid= classid, subjectid= subjectid))
        df = pd.DataFrame.from_dict(ClassPoint)
        Lop = df['Lớp'][0]
        subject = df['Môn học'][0]
        diem = np.round(df['Điểm tổng kết'].mean(), 1)
        return f'Điểm trung bình môn {subject} của lớp {Lop} là {diem}'
    else: 
        raise HTTPException(status_code=404, detail="Chưa có thông tin nào về học sinh được đưa ra (studentid: int, subjectid: int)")

@app.post('/student/ThemHocSinh', tags= ['Thêm học sinh'])
def post_student(student : schemas.Student, db : Session = Depends(get_db)):
    hocSinhMoi = models.Student(
                    id = student.id,
                    name = student.studentName,
                    classId = student.classIn
                    )
    return hocSinhMoi
#endregion    
@app.get('/student/HocLucHocSinh', tags= ['Học lực của học sinh'])
def get_HocLuc(
    studentid : Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if( studentid != None):
        studentInClass = data.SubjectAndStudentMethod.get_all_student(db, studentid=studentid)
        df = pd.DataFrame.from_dict(studentInClass)
        diem = df['Điểm tổng kết']
        name = df['Họ và tên'][0]
        diemTrungBinh = np.round(diem.sum()/ len(df['Điểm tổng kết'].to_list()), 1)
        if diemTrungBinh >=8:
            return {'result': f'{name} đã là học sinh giỏi với {diemTrungBinh} điểm tổng kết'}            
        elif diemTrungBinh >=6.5:
            return {'result': f'{name} đã là học sinh khá với {diemTrungBinh} điểm tổng kết'}
        elif diemTrungBinh >= 5:
            return {'result': f'{name} đã là học sinh trung bình với {diemTrungBinh} điểm tổng kết'}
        elif diemTrungBinh >= 4: 
            return {'result': f'{name} là học sinh yếu với {diemTrungBinh} điểm tổng kết'}
        else:
            return {'result': f'{name} đã bị đúp với {diemTrungBinh} điểm tổng kết'}
    else: 
        raise HTTPException(status_code=404, detail={
            "field": "studentid",
            "errMsg": "Chưa có thông tin"
        })

#region DucAnh
#pd:
@app.get('/statistic/subject/{subjectid}')
def get_point_subject_class(subjectid: int, db: Session = Depends(get_db)):
    if(subjectid > 0) :
        getSubject = data.SubjectMethod.get_all(db)
        if subjectid > len(getSubject):
            return {
                "msg": "Không tồn tại môn học"
            }
        else:
            listStudentSubject = data.SubjectStudentPointMethod.get_point_subjectid(db, subjectid)
            if len(listStudentSubject) != 0:
                df = pd.DataFrame.from_dict(listStudentSubject)
                classList = df.groupby(df['Lớp']).mean(numeric_only = True).applymap(lambda x: np.round(x, 2))
                subjectName = df['Môn học'][0]
                return {
                    "msg": f"Thống kê điểm tổng kết theo lớp môn {subjectName}",
                    "data" : classList.T
                }
            else:
                return {
                    "msg": "Không tồn tại bản ghi nào"
                }
    else:
        raise HTTPException(status_code=404, detail={
                "field" : "subjectid",
                "errMsg" : "Giá trị subjectid không thể nỏ hơn hoặc bằng 0"
            })

@app.post('/class/TimKiemHocSinh')
def post_find_student(studentInfor: schemas.StudentFind, db: Session = Depends(get_db)):
    result = ""
    errorList = []
    line = 0
    for dict in studentInfor:
        if(line >= 2):
            if dict[1] < 0:    
                errorList.append({"field": dict[0], "errMsg" : "Điểm nhỏ hơn 0"})
            elif dict[1] >10:
                errorList.append({"field": dict[0], "errMsg" : "Điểm lớn hơn 10"})
        else:
            if line!=1:
                if dict[1] <= 0:    
                    errorList.append({"field": dict[0], "errMsg" : "id Không được nhỏ hơn hoặc bằng 0"})
        line +=1
    if len(errorList) > 0:
        result = errorList
    else:
        list_avai = data.ClassAndStudentAndPointMethod.find_student_point(db, studentInfor)
        if(len(list_avai) !=0): 
            df = pd.DataFrame.from_dict(list_avai)
            result = df.T
        else:
            result = {
                "msg": "không có kết quả phù hợp"
            }
    return result

#np:
@app.get('/subject/DiemTongKetTrungBinhHocSinh')
def get_avg_point_subject(
    studentid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if( studentid != None):
        if(studentid >0):
            studentInClass = data.SubjectAndStudentMethod.get_all_student(db, studentid=studentid);
            df = pd.DataFrame.from_dict(studentInClass)
            
            diemTrungBinh = np.round(df['Điểm tổng kết'].sum() / len(df['Điểm tổng kết'].to_list()), 1)
            name = df['Họ và tên'][0]
            return {
                "msg": f'Điểm trung bình của {name} là: {diemTrungBinh}',
                "data": diemTrungBinh}
        else:
            raise HTTPException(status_code=404, detail={
                "field": "studentid",
                "errMsg": "Phải lớn hơn 0"
            })
    else: 
        raise HTTPException(status_code=404, detail={
            "field": "studentid",
            "errMsg": "Chưa có thông tin"
        })


@app.post('/subject/CapNhatDiemTrungBinhMon', tags=['Cập nhật điểm trung bình'])
def post_avg_point(pointList: schemas.SubjectAvgPoint ,db: Session = Depends(get_db)):
    result = ""
    errorList = []
    line = 0
    for dict in pointList:
        if(line >= 2):
            if dict[1] < 0:    
                errorList.append({"field": dict[0], "errMsg" : "Điểm nhỏ hơn 0"})
            elif dict[1] >10:
                errorList.append({"field": dict[0], "errMsg" : "Điểm lớn hơn 10"})
        else:
            if dict[1] <= 0:    
                errorList.append({"field": dict[0], "errMsg" : "id Không được nhỏ hơn hoặc bằng 0"})
        line +=1
    if len(errorList) > 0:
        result = errorList
    else:
        if np.array(data.SubjectStudentPointMethod.get_student_point(db, schemas.SubjectStudentPointBase(studentId=pointList.studentId, subjectId=pointList.subjectId))).size != 0:
            pointCal = np.round(
                (pointList.fiftFirstPoints * 0.15 + pointList.midtermPoint *0.35) + 
                (pointList.fiftSecPoints * 0.15 + pointList.lastTermPoint *0.35)
                , 2)
            updateData = data.SubjectStudentPointMethod.update_point(db, schemas.SubjectStudentPointCreate(
                studentId=pointList.studentId,
                subjectId=pointList.subjectId,
                pointFifFirst = pointList.fiftFirstPoints,
                pointFifSec = pointList.fiftSecPoints,
                pointFirstLast = pointList.midtermPoint,
                pointSecLast = pointList.lastTermPoint, 
                finnalSum = np.round(((pointList.fiftFirstPoints * 0.3 + pointList.midtermPoint *0.7)+(pointList.fiftSecPoints * 0.3 + pointList.lastTermPoint *0.7))/2 ,1)
                ))
            result = {
                "Họ và tên": data.StudentMethod.get_byid(db, pointList.studentId)[0].Name,
                "Môn học" : data.SubjectMethod.get_subject_id(db, pointList.subjectId)[0].name,
                "Điểm": updateData.finnalSum
            }
        else:
            if np.array(data.SubjectMethod.get_subject_id(db, pointList.subjectId)).size == 0:
                result = {
                    "field": "subjectId",
                    "errMsg" : "Không tồn tại môn học"
                }
            elif np.array(data.StudentMethod.get_byid(db, studentid = pointList.studentId)).size == 0:
                result = {
                    "field": "studentId",
                    "errMsg" : "Không tồn tại học sinh"
                }
            
    return result

#endregion

#region Hieu

#region pandas câu 1

@app.get('/student_score/whoHasIncreasedTheirScores', tags=['Danh sách học sinh có điểm tăng dần theo từng bài kiểm tra'])
def get_highest_forward(
    db: Session = Depends(get_db)
):
    studentList = data.StudentWithIncreasingScoresMethod.get_list(db)
    table = pd.DataFrame.from_dict(studentList).to_html()
    text_file = open("student_list_1.html", "w")
    text_file.write(table)
    text_file.close()
    webbrowser.open(os.getcwd() + '/student_list_1.html')
    return f'Kết quả được hiển thị ở cửa sổ mới...'

#endregion

#region pandas câu 2 có ý tưởng thì đổi sau

@app.post('/student/classesScoresBySubject', tags=['Thống kê điểm trung bình của từng lớp theo môn học'])
def post_class_scores_by_subject(
    gradeSubject: schemas.ClassAndSubject,
    db: Session = Depends(get_db)
):
    studentList = data.ClassAndSubjectMethod.get_list(gradeSubject, db)
    table = pd.DataFrame.from_dict(studentList).to_html()
    text_file = open("student_list_2.html", "w")
    text_file.write(table)
    text_file.close()
    webbrowser.open(os.getcwd() + '/student_list_2.html')
    return f'Kết quả được hiển thị ở cửa sổ mới...'
    
#endregion

#endregion

# @app.post('/class', response_model = schemas.ClassBase)
# def create_class(classroom: schemas.ClassBase, db: Session = Depends(get_db)):
#     return data.ClassroomMethod.create_class(db, classroom)

# @app.post('/subject', response_model = schemas.SubjectBase)
# def create_subject(subject: schemas.SubjectBase, db: Session = Depends(get_db)):
#     return data.SubjectMethod.create_subject(db, subject)




# region Dũng
# np
@app.get('/subject/SinhVienTruotMon')
def get_point_less_than_4 (
    studentid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if (studentid != None):
        studentFailed = data.SubjectAndStudentMethod.get_all_student(db, studentid)
        if np.array(studentFailed).size != 0:
            df = pd.DataFrame.from_dict(studentFailed)
            print(df)
            diem = df['Điểm tổng kết'][0]
            name = df['Họ và tên'][0]
            subject = df['Môn học'][0]
            if diem < 4:
                return f'{name} trượt môn {subject} với số điểm {diem}'
            else:
                return f'{name} qua môn {subject} với số điểm {diem}'
        else:
            raise HTTPException(status_code=404, detail={
                "field": "studentid",
                "errMsg": "Chưa có thông tin (studentid: int)"
            })
    else:
        raise HTTPException(status_code=404, detail=
            "Chưa có thông tin (studentid: int, subjectid: int)"
        )

@app.post('/subject/GetClassSize')
def Send_Id_Get_NumStu(
    classID: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if (classID):
        classSz = data.GetStudentInClass.getStuIn4(classID = classID, db = db)
        num_students = np.sum(classSz)
        return num_students
    else:
        raise HTTPException(status_code=404, detail=
            "Mã lớp không tồn tại hoặc không hợp lệ !"
        )


def Send_Id_Get_NumStu(classID: int, db: Session = Depends(get_db)):
    students = data.GetStudentInClass.getStu(classID=classID, db=db)
    num_students = len(students)
    return num_students



# pd
@app.post('/statistic/class/grade')
def post_static(classAndPoint: schemas.ClassAndSubject, db: Session = Depends(get_db)):
    resClass = data.ClassAndStudentAndPointMethod.get_all_point(db, classAndPoint)
    df = pd.DataFrame.from_dict(resClass)
    print(df)
    if (classAndPoint.grade < 10 or classAndPoint.grade > 12):
        return "Dữ liệu chỉ có trong các khối lớp cấp 3!"
    elif (classAndPoint.subjectid < 0 or classAndPoint.subjectid > 10):
        return "Chỉ có dữ liệu môn học từ 1-10"
    else:
        # grCol = (df['Khối'] == classAndPoint.grade).groupby(df['Khối'] == classAndPoint.subjectid)
        # max_Point = df.idxmax(df['Điểm tổng kết'])

        # # Lấy in4 học sinh max
        # infStuMax = df.loc[max_Point_wGrade][['Môn', 'Khối', 'Họ và tên', 'Điểm tổng kết']]
        # return df.loc[infStuMax][['Môn', 'Khối', 'Họ và tên', 'Điểm tổng kết']]
        return df.T


@app.get('/subject/SoSVTruotMonMoiMonHoc', tags= ['Số học sinh trượt mỗi môn'])
def get_number_of_failed_students_per_subject(db: Session = Depends(get_db)):
    all_Point = data.SubjectAndStudentMethod.get_all_student_all(db)
    df = pd.DataFrame.from_dict(all_Point)
    print(df)
    df['Trượt'] = np.where(df['Điểm tổng kết'] < 4, 'Trượt', 'Không trượt')
    df_subjects = df[['Môn học', 'Trượt']]

    # Số học sinh trượt môn học theo từng môn
    df_failed = df_subjects[df_subjects['Trượt'] == 'Trượt'].groupby(['Môn học']).size().reset_index(name='Số lượng')
    
    html_chart = df_failed.to_html()
    return html_chart

# endregion
