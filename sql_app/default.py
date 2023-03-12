import sqlite3
import numpy as np 
import random
import string

def initDef():
    connect = sqlite3.connect('DiemSinhVien_Python_K2N2_test.db')
    c = connect.cursor()

    startGrade = 10
    endGrade = 12
    classRoom = 6
    for eachGrade in range (startGrade, endGrade+1):
        for eachClass in range (1, classRoom+1):
            c.execute('''INSERT INTO "class"("name","grade") VALUES (?, ?)''', [f'{eachGrade}A{eachClass}', f'{eachGrade}'])
 

    studentEachClass = 30
    studentSum = classRoom * studentEachClass
    middleNameList = ["Hoàng", "Văn", "Quang", "Quốc", "Thị", "Minh"]
    firstNameList = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương" ,"Lý"]

    def classIsReady(classId, studentEachClass, classRoom):
        studentInClass = c.execute('''SELECT * FROM "student" WHERE classId == ?''', [classId])
        
        if(len(studentInClass.fetchall()) < studentEachClass):
            return classId
        else:
            classIdNew = int(np.ceil(classRoom*np.random.random()))
            studentEachClassNew = studentEachClass
            classRoomNew = classRoom
            return classIsReady(classIdNew, studentEachClassNew, classRoomNew)
    def setStudentToClass(classId):
        firstName = firstNameList[int(np.floor(len(firstNameList) * np.random.random()))]
        middleName =  middleNameList[int(np.floor(len(middleNameList) * np.random.random()))]
        lastName = random.choices(string.ascii_uppercase, k=1)
        c.execute('''INSERT INTO "student"("name", "classId") VALUES (? ,?)''', [f'{firstName} {middleName} {lastName[0]}', classId])

    for eachstudent in range (0, studentSum):
        classId = int(np.ceil(classRoom * np.random.random()))
        setStudentToClass(classIsReady(classId, studentEachClass, classRoom))


    listSubject = [
        ["Toán"],
        ["Văn"],
        ["Tiếng Anh"],
        ["Vật lý"],
        ["Hóa học"],
        ["Sinh học"],
        ["Lịch sử"],
        ["Địa lý"],
        ["Giáo dục công dân"],
        ["Thể dục"]
    ]
    c.executemany('''INSERT INTO "subject"("name") VALUES (?)''', listSubject)

    for student in range(0, studentSum):
        subjectLen = c.execute('''SELECT * FROM "subject" ''')
        for subject in range(0, len(subjectLen.fetchall())):
            c.execute('''INSERT INTO "subjectStudent" VALUES (?,?,?) ''', [student+1, subject +1, np.round(np.random.random()*10 , 2)])
        
        
    connect.commit()
    connect.close()