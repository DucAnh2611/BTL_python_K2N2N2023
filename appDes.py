description = """
Bài tập lớn môn **Lập trình python**
## Thành viên nhóm
* **A38253 Nguyễn Hoàng Đức Anh**
* **A38520 Mai Văn Mạnh**
* **A38911 Vũ Tiến Dũng**
* **A41174 Hoàng Chí Hiếu** (_Trưởng nhóm_).
"""
tags_metadata = [
    {
        "name" : "Trang chủ",
        "description" : "Hiển thị thông tin của nhóm và thông tin thành viên"
    },
    {
        "name" : "Đức Anh Numpy",
        "description" : "Cập nhập thông tin Điểm trung bình và lấy điểm tổng kết của học sinh"
    },
    {
        "name" : "Đức Anh Pandas",
        "description" : "Thống kê điểm của môn theo lớp và Tìm kiếm học sinh có thông tin"
    },
    {
        'name' : 'Mạnh Pandas',
        "description": 'Hiển thị bảng điểm của học sinh theo mã học sinh và Cập nhật tên lớp và khối theo mã lớp'
    },
    {
        'name' : 'Mạnh Numpy',
        "description": 'Hiển thị điểm trung bình môn theo mã lớp, mã môn và Hiển thị điểm trung bình 2 môn của học sinh theo mã của 2 môn và mã học sinh'
    },
    {
        'name' : 'Hiếu Numpy',
        'description': 'Các API ứng dụng Numpy'
    },
    {
        'name' : 'Hiếu Pandas',
        'description': 'Các API ứng dụng Pandas'
    }
]
descriptionApi = {
    "DucAnhPd": {
        "ThongKeMonHoc" : "Nhập mã môn học để nhận lại thông tin trả về là 1 bảng các lớp học có số điểm của môn học. subjectid mang giá trị số nguyên dương",
        "TimKiemHocSinh": "Nhập một trong các thoomg tin cá nhân của học sinh để nhận lại thông tin của bảng chứa các thông tin cần tìm"
    },
    "DucAnhNp" : {
        "DiemTongKetTrungBinhHocSinh": "Nhập mã học sinh để nhận lại điểm tổng kết trung bình (Trung bình của tất cả các môn)",
        "CapNhatDiemTrungBinhMon": "Nhập các thông tin: studentid, subjectid, điểm 15 phút 2 lần, điểm cuối kỳ 2 lần với method post sau đó sẽ tự động cập nhật thông tin của sinh viên ở môn học đó trong cơ sở dữ liệu"
    },
    'HieuNP' : {
        'BangXepHang' : 'Hiện bảng xếp hạng điểm tổng kết và học lực tương ứng',
        'TinhTichPhan' : 'Tính tích phân dựa theo các thông số đầu vào'
    },
    'HieuPD' : {
        'DanhSachHocSinhTienBo' : 'Hiển thị những học sinh có điểm các bài kiểm tra tăng dần',
        'ThongKeDiemSo' : 'Thống kê điểm trung bình của từng lớp (từng khối) theo môn học'
    }
    
}
