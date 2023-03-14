from fastapi import FastAPI, Depends, FastAPI, HTTPException
from starlette.responses import FileResponse 
from sqlalchemy.orm import Session
from typing import Union
import numpy as np
import pandas as pd
import sql_app.models as models
import sql_app.schemas as schemas
import sql_app.data as data
from database import SessionLocal, engine, get_db
from sql_app.default import initDef 
from fastapi.responses import HTMLResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# initDef()

@app.get('/', response_class=HTMLResponse)
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
                <li>A????? Hoàng Chí Hiếu</li>
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

@app.get('/subject/DiemCuaMon')
def get_max_point_subject(
    studentid: Union[int, None] = None,
    subjectid: Union[str, None] = None,
    db: Session = Depends(get_db)
):
    if(studentid != None or subjectid !=None):
        studentInClass= data.SubjectPointMethod.get_student_point(db, studentid=studentid, subjectid= subjectid);
        df = pd.DataFrame.from_dict(studentInClass)
        diem = df['Điểm'][0]
        name = df['Họ và tên'][0]
        subject = df['Môn học'][0]
        return f'Điểm của {name} với môn {subject} là: {diem}'
    else: 
        raise HTTPException(status_code=404, detail="Chưa có thông tin nào về học sinh được đưa ra (studentid: int, subjectid: int)")
    
#DucAnh
#pd:
@app.get('/subject/DiemTongKetTrungBinhHocSinh')
def get_class_point_subject(
    studentid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if( studentid != None):
        studentInClass = data.SubjectAndStudentMethod.get_all_student(db, studentid=studentid);
        df = pd.DataFrame.from_dict(studentInClass)
        df['Điểm'] = df['Điểm'].fillna(0)
        diemTrungBinh = np.round(df['Điểm'].sum() / len(df['Điểm'].to_list()), 1)
        name = df['Họ và tên'][0]
        return f'Điểm trung bình của {name} là: {diemTrungBinh}'
    else: 
        raise HTTPException(status_code=404, detail={
            "field": "studentid",
            "errMsg": "Chưa có thông tin"
        })

#np:
@app.post('/subject/CapNhapDiemTrungBinhMon')
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
        if data.SubjectStudentPointMethod.get_student_point(db, schemas.SubjectStudentPointBase(studentId=pointList.studentId, subjectId=pointList.subjectId)):
            pointCal = np.round(
                (pointList.fiftFirstPoints * 0.15 + pointList.midtermPoint *0.35) + 
                (pointList.fiftSecPoints * 0.15 + pointList.lastTermPoint *0.35)
                , 2)
            updateData = data.SubjectStudentPointMethod.update_point(db, schemas.SubjectStudentPointCreate(studentId=pointList.studentId, subjectId=pointList.subjectId, point=pointCal))
            result = {
                "Họ và tên": data.StudentMethod.get_byid(db, pointList.studentId)[0]['Name'],
                "Môn học" : data.SubjectMethod.get_subject_id(db, pointList.subjectId)[0].name,
                "Điểm": updateData.point
            }
        else:
            if data.SubjectMethod.get_subject_id(db, pointList.subjectId):
                errorList.append({
                    "field": "subjectId",
                    "errMsg" : "Không tồn tại môn học"
                })
            elif data.StudentMethod.get_byid(db, studentid= pointList.studentId):
                errorList.append({
                    "field": "studentId",
                    "errMsg" : "Không tồn tại học sinh"
                })
            result = errorList
    return result

# @app.post('/class', response_model = schemas.ClassBase)
# def create_class(classroom: schemas.ClassBase, db: Session = Depends(get_db)):
#     return data.ClassroomMethod.create_class(db, classroom)

# @app.post('/subject', response_model = schemas.SubjectBase)
# def create_subject(subject: schemas.SubjectBase, db: Session = Depends(get_db)):
#     return data.SubjectMethod.create_subject(db, subject)
