from fastapi import FastAPI, Depends, FastAPI, HTTPException
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

@app.get('/subject/DiemTongKetTrungBinhHocSinh')
def get_class_point_subject(
    studentid: Union[int, None] = None,
    studentname: Union[str, None] = None,
    db: Session = Depends(get_db)
):
    if( studentid != None or studentname != None):
        studentInClass= data.SubjectAndStudentMethod.get_all_student(db, studentid=studentid, studentname=studentname);
        df = pd.DataFrame.from_dict(studentInClass)
        diemTrungBinh = np.round(df['Điểm'].sum() / len(df['Điểm'].to_list()), 1)
        name = df['Họ và tên'][0]
        return f'Điểm trung bình của {name} là: {diemTrungBinh}'
    else: 
        raise HTTPException(status_code=404, detail="Chưa có thông tin nào về học sinh được đưa ra (studentid: int, studentname: str)")

@app.get('/subject/DiemCuaMon')
def get_max_point_subject(
    studentid: Union[int, None] = None,
    studentname: Union[str, None] = None,
    subjectid: Union[str, None] = None,
    db: Session = Depends(get_db)
):
    if(studentid != None or studentname != None or subjectid !=None):
        studentInClass= data.SubjectPointMethod.get_student_point(db, studentid=studentid, studentname=studentname, subjectid= subjectid);
        df = pd.DataFrame.from_dict(studentInClass)
        diem = df['Điểm'][0]
        name = df['Họ và tên'][0]
        subject = df['Môn học'][0]
        return f'Điểm của {name} với môn {subject} là: {diem}'
    else: 
        raise HTTPException(status_code=404, detail="Chưa có thông tin nào về học sinh được đưa ra (studentid: int, studentname: str, subjectid: int)")

# @app.post('/class', response_model = schemas.ClassBase)
# def create_class(classroom: schemas.ClassBase, db: Session = Depends(get_db)):
#     return data.ClassroomMethod.create_class(db, classroom)

# @app.post('/subject', response_model = schemas.SubjectBase)
# def create_subject(subject: schemas.SubjectBase, db: Session = Depends(get_db)):
#     return data.SubjectMethod.create_subject(db, subject)
