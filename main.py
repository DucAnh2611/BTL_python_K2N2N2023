from fastapi import FastAPI, Depends, FastAPI, HTTPException, Path, File, UploadFile, status
from starlette.responses import FileResponse 
from sqlalchemy.orm import Session
from typing import Union
import appDes as appDes
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

app = FastAPI(
    title="Quản lý điểm học sinh",
    description=appDes.description,
    version="1.0.0",
    contact={
        "name": "Source Code",
        "url": "https://github.com/DucAnh2611/BTL_python_K2N2N2023",
    },
    openapi_tags=appDes.tags_metadata
)
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

@app.get('/subject/DiemTongKetCuaHocSinh/{studentid}', 
         tags=['Mạnh Pandas'],
         description=appDes.descriptionApi['Mạnh Pandas']['DiemTongKetCuaHocSinh'])
def get_student_point_subject(
    studentid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if( studentid != None):
        if studentid > 0:
            studentInClass = data.SubjectAndStudentMethod.get_all_student(db, studentid=studentid)
            df = pd.DataFrame.from_dict(studentInClass)
            df['Điểm tổng kết'] = df['Điểm tổng kết']
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
            "errMsg": "Thông tin không hợp lệ"
        })
            
    else: 
        raise HTTPException(status_code=404, detail={
            "field": "studentid",
            "errMsg": "Chưa có thông tin"
        })

@app.post('/class/CapNhatTenLop', 
          tags=['Mạnh Pandas'],
          description=appDes.descriptionApi['Mạnh Pandas']['CapNhatTenLop'])
def post_classroom(classroom: schemas.Classroom, db : Session = Depends(get_db)):
    result = " "
    if classroom.classid >0 :
        updateData = data.ClassroomMethod.update_class(db, schemas.Classroom(
            className= classroom.className,
            classGrade= classroom.classGrade,
            classid= classroom.classid
            ))
        result = data.ClassroomMethod.get_class(db, classroom.classid)
    else:
        result = {
            "field": "classid",
            "errMsg": "Thông tin không hợp lệ"
        }

    return result

#np
@app.get('/subject/ClassSubjectAvgPoint/{classid}/{subjectid}', 
         tags= ['Mạnh Numpy'], 
         description=appDes.descriptionApi['Mạnh Numpy']['ClassSubjectAvgPoint'])
def get_Class_Subject_Avg_Point(
    classid: Union[int, None] = None, 
    subjectid: Union[int, None] = None,
    db: Session = Depends(get_db)
):
    if(classid != None or subjectid != None):
        ClassPoint = data.GradePointMethod.get_SubjectPointfromClass(db, schemas.ClassPoint(classid= classid, subjectid= subjectid))
        df = pd.DataFrame.from_dict(ClassPoint)
        Lop = df['Lớp'][0]
        subject = df['Môn học'][0]
        diemTK= np.array([df['Điểm tổng kết']])
        diem = np.round(np.mean(diemTK), 1)
        return f'Điểm trung bình môn {subject} của lớp {Lop} là {diem}'
    else: 
        raise HTTPException(status_code=404, detail="Chưa có thông tin nào về học sinh được đưa ra (studentid: int, subjectid: int)")

@app.post('/student/Avg2Subject', tags= ['Mạnh Numpy'],
          description=appDes.descriptionApi['Mạnh Numpy']['Avg2Subject'])
def Avg_2_subject(
    student: schemas.avg2sub,
    db: Session = Depends(get_db)
):
    if student.studentid != None or student.subject1 != None or student.subject2 != None :
        if student.studentid > 0 :
            if student.subject1 > 0 and student.subject2 >0:
                studentPoint1= data.SubjectStudentPointMethod.get_student_point(db, schemas.SubjectStudentPointBase(studentId=student.studentid, subjectId=student.subject1))
                studentPoint2= data.SubjectStudentPointMethod.get_student_point(db, schemas.SubjectStudentPointBase(studentId=student.studentid, subjectId=student.subject2))
                df1 = pd.DataFrame.from_dict(studentPoint1)
                df2 = pd.DataFrame.from_dict(studentPoint2)
                diemMon1 = df1['Điểm tổng kết'][0]
                diemMon2 = df2['Điểm tổng kết'][0]
                subject1 = df1['Môn học'][0]
                subject2 = df2['Môn học'][0]
                name = df1['Họ và tên'][0]
                diem = np.array([diemMon1, diemMon2])
                diemTrungBinh = np.round(np.mean(diem) ,1)
            else:
                raise HTTPException(status_code=404, detail={
                "field": "subject1, subject2",
                "errMsg": "Thông tin không hợp lệ"
                })
        else: 
            raise HTTPException(status_code=404, detail={
            "field": "studentid",
            "errMsg": "Thông tin không hợp lệ"
            })
    else:
        raise HTTPException(status_code=404, detail={
            "field": "studentid, subject1, subject2",
            "errMsg": "Chưa có thông tin"
        })
    return f'Điểm trung bình hai môn {subject1} và {subject2} của {name} là {diemTrungBinh}'


#endregion    

#region DucAnh
#pd:
@app.get('/statistic/subject/{subjectid}', tags=['Đức Anh Pandas'], description=appDes.descriptionApi['DucAnhPd']['ThongKeMonHoc'])
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
                "errMsg" : "Giá trị subjectid không thể nhỏ hơn hoặc bằng 0"
            })

@app.post('/class/TimKiemHocSinh', tags=['Đức Anh Pandas'], description=appDes.descriptionApi['DucAnhPd']['TimKiemHocSinh'])
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
            dfsize = len(df.index)
            result = {
                "msg" : f"có {dfsize} kết quả phù hợp",
                "data" : df.T
            }
        else:
            result = {
                "msg": "không có kết quả phù hợp"
            }
    return result

#np:
@app.get('/subject/DiemTongKetTrungBinhHocSinh', tags=['Đức Anh Numpy'], description = appDes.descriptionApi['DucAnhNp']['DiemTongKetTrungBinhHocSinh'])
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


@app.post('/subject/CapNhatDiemTrungBinhMon', tags=['Đức Anh Numpy'], description = appDes.descriptionApi['DucAnhNp']['CapNhatDiemTrungBinhMon'])
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

#region numpy câu 1

@app.get('/statistic/ranking',
         tags = ['Hiếu Numpy'],
         description=appDes.descriptionApi['HieuNP']['BangXepHang'])

def get_ranking(
    db: Session = Depends(get_db)
):
    scoreboard = data.OnlyScoreMethod.get_list(db)
    df = pd.DataFrame.from_dict(scoreboard)
    df['Học lực'] = get_evaluation(df['Điểm tổng kết'])
    table = pd.DataFrame.from_dict(df).to_html()
    
    return HTMLResponse(content=table, status_code=200)

@np.vectorize
def get_evaluation(score):
    if score > 8.5: 
        return 'Giỏi'
    elif score > 6.5:
        return 'Khá'
    elif score > 5:
        return 'Trung bình'
    else:
        return 'Kém'
    

#endregion

#region numpy câu 2

@app.post('/default/calculateIntegration',
          tags=['Hiếu Numpy'],
          description=appDes.descriptionApi['HieuNP']['TinhTichPhan'])
def integration_calculation(
    input: schemas.IntegrationInput
):
    funcs = ['ln', 'log', 'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'sec', 'sinh', 'arsinh', 'power']
    result = input.equation
    for func in funcs:
        result = result.replace(func, f'np.{func}')
    x = np.linspace(input.lower_bound, input.upper_bound, 1000000)
    try:
        return f'Kết quả: {np.trapz(eval(result), x)}'
    except:
        raise HTTPException(status_code=500, detail={
            "field": "equation",
            "errMsg": "phương trình không hợp lệ! Vui lòng kiểm tra lại"
        })


#endregion

#region pandas câu 1

@app.get('/statistic/whoHasIncreasedTheirScores', 
         tags=['Hiếu Pandas'],
         description=appDes.descriptionApi['HieuPD']['DanhSachHocSinhTienBo'])
def who_has_increased_their_scores(
    db: Session = Depends(get_db)
):
    studentList = data.StudentWithIncreasingScoresMethod.get_list(db)
    if len(studentList) != 0:
        table = pd.DataFrame.from_dict(studentList).to_html()
        return HTMLResponse(content=table, status_code=200)
    else:
        return {
            "msg": "Không tồn tại bản ghi nào!"
        }

#endregion

#region pandas câu 2

@app.post('/statistic/classesScoresBySubject', 
          tags=['Hiếu Pandas'],
          description=appDes.descriptionApi['HieuPD']['ThongKeDiemSo'])
def class_scores_by_subject(
    gradeSubject: schemas.ClassAndSubject,
    db: Session = Depends(get_db)
):
    if(gradeSubject.subjectid > 0):
        getSubject = data.SubjectMethod.get_all(db)
        if gradeSubject.subjectid > len(getSubject):
            return {
                "msg": "Không tồn tại môn học"
            }
        else:
            studentList = data.ClassAndSubjectMethod.get_list(gradeSubject, db)
            if len(studentList) != 0:
                table = pd.DataFrame.from_dict(studentList)
                table['Điểm trung bình'] = table['Điểm trung bình'].round(decimals=2)
                return HTMLResponse(content = table.to_html(), status_code=200)
            else:
                return {
                    "msg": "Không tồn tại bản ghi nào!"
                }
    else:
        raise HTTPException(status_code=404, detail={
                "field" : "subjectid",
                "errMsg" : "Giá trị subjectid không thể nhỏ hơn hoặc bằng 0"
            })

#endregion

#endregion

#region Dũng
# np
@app.get('/subject/SinhVienTruotMonToan',
            tags=['Dũng Numpy'],
            description=appDes.descriptionApi['DungNumpy']['SinhVienTruotMonToan']
        )

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
            "Chưa có thông tin (studentid: int)"
        )

@app.post('/subject/GetClassSize',
            tags=['Dũng Numpy'],
            description=appDes.descriptionApi['DungNumpy']['SiSoLopTheoID']
        )
def Send_Id_Get_ClassSz(
    classID: schemas.ClassID, 
    db: Session = Depends(get_db)
):
    if (classID.classID != None and classID.classID > 0):
        classSz = data.GetStudentInClass.getStuIn4(classID = classID.classID, db = db)
        fullClass = data.ClassroomMethod.get_all(db = db)
        # Tổng số học sinh trong lớp
        num_Stu_inClass = len(np.array(classSz))
        # Tổng số lớp
        allC = len(np.array(fullClass))
        
        if (classID.classID > allC):
            return f"Mã lớp {classID.classID} không tồn tại !"
        else:
            return f"Sĩ số lớp có mã lớp {classID.classID} là {num_Stu_inClass} học sinh"
    else:
        raise HTTPException(status_code=404, detail=
            f"Mã lớp {classID.classID} không hợp lệ !"
        )




# pd
@app.post('/statistic/class/grade',
            tags=['Dũng Pandas'],
            description=appDes.descriptionApi['DungPandas']['ThongTinHSDiemCaoNhatVaThapNhat']
        )
def post_static(classAndPoint: schemas.ClassAndSubject, db: Session = Depends(get_db)):
    resClass = data.ClassAndStudentAndPointMethod.get_all_point(db, classAndPoint)
    df = pd.DataFrame.from_dict(resClass)
    if (classAndPoint.grade < 10 or classAndPoint.grade > 12):
        return "Dữ liệu chỉ có trong các khối lớp cấp 3!"
    elif (classAndPoint.subjectid < 0 or classAndPoint.subjectid > 10):
        return "Chỉ có dữ liệu môn học từ 1-10"
    else:
        max_Point = df['Điểm tổng kết'].idxmax()
        min_Point = df['Điểm tổng kết'].idxmin()

        # # Lấy in4 học sinh max, min
        in4HS_max = df.iloc[[max_Point]]
        in4HS_min = df.iloc[[min_Point]]

        return {
            "Highest": {
                "msg": f"Học sinh điểm cao nhất mã môn {classAndPoint.subjectid} khối {classAndPoint.grade}",
                "data": in4HS_max.T
            },
            "Lowest": {
                "msg": f"Học sinh điểm thấp nhất mã môn {classAndPoint.subjectid} khối {classAndPoint.grade}",
                "data": in4HS_min.T
            }
        }


@app.get('/subject/SoHSTruotMonMoiMonHoc',
            tags=['Dũng Pandas'],
            description=appDes.descriptionApi['DungPandas']['TongSoHSTruotCacMon']
        )
def get_number_of_failed_students_per_subject(db: Session = Depends(get_db)):
    all_Point = data.SubjectAndStudentMethod.get_all_student_all(db)
    df = pd.DataFrame.from_dict(all_Point)
    df['Trượt'] = np.where(df['Điểm tổng kết'] < 4, 'Trượt', 'Không trượt')
    df_subjects = df[['Môn học', 'Trượt']]
    
    # Số học sinh trượt môn học theo từng môn
    df_failed = df_subjects[df_subjects['Trượt'] == 'Trượt'].groupby(['Môn học']).size().reset_index(name='Tổng số HS trượt')
    
    html_chart = df_failed.to_html()
    return HTMLResponse(content=html_chart, status_code=200)

# endregion
