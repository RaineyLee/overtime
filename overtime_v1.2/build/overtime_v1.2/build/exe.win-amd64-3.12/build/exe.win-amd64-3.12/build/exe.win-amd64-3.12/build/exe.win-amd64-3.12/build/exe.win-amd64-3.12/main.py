import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic

# 절대경로를 상대경로로 변경 하는 함수
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#UI파일 연결
# main_window= uic.loadUiType(resource_path("/Users/black/projects/make_erp/main_window.ui"))[0] # Mac 사용시 ui 주소
main_window= uic.loadUiType(resource_path("./ui/main_window.ui"))[0] # Window 사용시 ui 주소

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, main_window) :
    def __init__(self) :
        super().__init__()

        self.version = 1.2

        from db.db_select import Select
        select = Select()
        result = select.select_version()

        if self.version == result[0][0]:
            self.setupUi(self)
            self.setWindowTitle("DOOCH PUMP HR")
            self.setFixedSize(QSize(1253,757))
        else:
            self.msg_box("확인", "사용중인 프로그램의 버전 확인이 필요합니다.")
            return
        
        self.slots()
            

    # def outgoing(self):
    #     print("new menu call")
    def slots(self):
        self.btn_send.clicked.connect(self.check_login)

    def check_login(self):        
        id = self.version
        password = self.txt_password.toPlainText()

        from db.db_select import Select
        select = Select()
        result = select.select_password(id)

        if password == result[0]:
            self.lbl_pass.setText("")
            self.txt_password.hide()
            self.btn_send.hide()

            self.mainwindow()
        else:
            self.txt_password.setText("")
            self.txt_password.setAlignment(Qt.AlignCenter)
            self.msg_box("오류", "사용자 코드를 확인 하세요.")


    def mainwindow(self):
        menu_bar = self.menuBar()
        hr_menu = menu_bar.addMenu("인사정보")
        overtime_info = menu_bar.addMenu("잔업시간 조회")
        overtime_upload = menu_bar.addMenu("잔업시간 입력")
        
        select_all = QAction('전체 조회', self)
        select_all.setStatusTip("전체 조회")
        select_all.triggered.connect(self.select_all)

        select_dept = QAction('부서별 조회', self)
        select_dept.setStatusTip("부서별 조회")
        select_dept.triggered.connect(self.select_dept)

        select_emp = QAction('사원별 조회', self)
        select_emp.setStatusTip("사원별 조회")
        select_emp.triggered.connect(self.select_emp)

        update_emp = QAction('잔업시간 수정', self)
        update_emp.setStatusTip("잔업시간 수정")
        update_emp.triggered.connect(self.update_emp)
        
        input_emp = QAction('잔업시간 입력', self)
        input_emp.setStatusTip("잔업시간 입력")
        input_emp.triggered.connect(self.input_emp)

        upload_overtime = QAction('잔업시간 업로드', self)
        upload_overtime.setStatusTip("잔업시간 업로드")
        upload_overtime.triggered.connect(self.upload_overtime)

        emp_master = QAction('인사정보', self)
        emp_master.setStatusTip("인사정보")
        emp_master.triggered.connect(self.emp_master)

        overtime_info.addAction(select_all)
        overtime_info.addAction(select_dept)
        overtime_info.addAction(select_emp)

        overtime_upload.addAction(update_emp)
        overtime_upload.addAction(input_emp)
        overtime_upload.addAction(upload_overtime)

        hr_menu.addAction(emp_master)

        status_bar = self.statusBar()
        self.setStatusBar(status_bar)

    def select_all(self):
        import total_overtime as total_overtime_window

        self.total_window = total_overtime_window.MainWindow()
        self.total_window.show()

    def select_dept(self):
        import dept_overtime as select_dept_window

        self.dept_window = select_dept_window.DeptMainWindow()
        self.dept_window.show()
    
    def select_emp(self):
        import emp_overtime as select_emp_window

        self.emp_window = select_emp_window.EmpMainWindow()
        self.emp_window.show() 
    
    def update_emp(self):
        import emp_overtime_update as update_emp_window

        self.emp_update_window = update_emp_window.MainWindow()
        self.emp_update_window.show() 

    def input_emp(self):
        import emp_overtime_input as input_emp_window

        self.emp_input_window = input_emp_window.MainWindow()
        self.emp_input_window.show() 

    def upload_overtime(self):
        import upload as upload_window

        self.upload_window = upload_window.MainWindow()
        self.upload_window.show()

    def emp_master(self):
        import emp_info as emp_info

        self.emp_master = emp_info.MainWindow()
        self.emp_master.show()

    def window_close(self):
        self.close()

    # def upload_location(self):        
    #     import upload_location as inv_loc

    #     self.location = inv_loc.WindowClass() #메인창에서 띄우려면 메인창을 뜻하는 self 추가
    #     self.location.show() #메인창에서 띄우려면 메인창을 뜻하는 self 추가

    # def upload_barcode(self):
    #     import upload_barcode as bar_loc

    #     self.barcode = bar_loc.WindowClass() #메인창에서 띄우려면 메인창을 뜻하는 self 추가
    #     self.barcode.show() #메인창에서 띄우려면 메인창을 뜻하는 self 추가

    # def upload_saleslist(self):
    #     import upload_saleslist as saleslist

    #     self.saleslist = saleslist.WindowClass() #메인창에서 띄우려면 메인창을 뜻하는 self 추가
    #     self.saleslist.show() #메인창에서 띄우려면 메인창을 뜻하는 self 추가

    # def item_location(self):
    #     import toexcel_location as item_loc

    #     self.item_loc = item_loc.WindowClass() #메인창에서 띄우려면 메인창을 뜻하는 self 추가
    #     self.item_loc.show() #메인창에서 띄우려면 메인창을 뜻하는 self 추가

    # def make_cjnumber(self):
    #     import CJ_number_v1_2 as cj_number

    #     self.cj_number = cj_number.WindowClass() #메인창에서 띄우려면 메인창을 뜻하는 self 추가
    #  self.cj_number.show() #메인창에서 띄우려면 메인창을 뜻하는 self 추가

    def msg_box(self, arg_1, arg_2):
        msg = QMessageBox()
        msg.setWindowTitle(arg_1)               # 제목설정
        msg.setText(arg_2)                          # 내용설정
        msg.exec_()       

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    try:
        myWindow = WindowClass()
        myWindow.show()
        app.exec_()
    except Exception as e:
        msg = QMessageBox()
        msg.setWindowTitle("Error")               # 제목설정
        msg.setText(str(e))                          # 내용설정
        msg.exec_()  