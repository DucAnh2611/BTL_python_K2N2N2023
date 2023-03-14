from fastapi import FastAPI, Depends, FastAPI, HTTPException, Path
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

#Manh
#np
@app.get('/subject/DiemTongKetCuaMon', tags=["Điểm tổng kết của môn"])
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

#DucAnh
#pd:
@app.get('/subject/DiemTongKetTrungBinhHocSinh', tags=['Điểm tổng kết trung bình'])
def get_class_point_subject(
    studentid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if( studentid != None):
        studentInClass = data.SubjectAndStudentMethod.get_all_student(db, studentid=studentid);
        df = pd.DataFrame.from_dict(studentInClass)
        df['Điểm tổng kết'] = df['Điểm tổng kết'].fillna(0)
        diemTrungBinh = np.round(df['Điểm tổng kết'].sum() / len(df['Điểm tổng kết'].to_list()), 1)
        name = df['Họ và tên'][0]
        return f'Điểm trung bình của {name} là: {diemTrungBinh}'
    else: 
        raise HTTPException(status_code=404, detail={
            "field": "studentid",
            "errMsg": "Chưa có thông tin"
        })

#np:
@app.get('/statistic/subject/{subjectId}')
def get_table_point_subject(subjectId : int):
    return {"subjectId": subjectId}


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

# @app.post('/class', response_model = schemas.ClassBase)
# def create_class(classroom: schemas.ClassBase, db: Session = Depends(get_db)):
#     return data.ClassroomMethod.create_class(db, classroom)

# @app.post('/subject', response_model = schemas.SubjectBase)
# def create_subject(subject: schemas.SubjectBase, db: Session = Depends(get_db)):
#     return data.SubjectMethod.create_subject(db, subject)
