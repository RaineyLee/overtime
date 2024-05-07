import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
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
main_window= uic.loadUiType(resource_path("c:.\\ui\\main_window.ui"))[0] # Window 사용시 ui 주소

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, main_window) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("인사정보 입력/조회")

        # self.slots()

        menu_bar = self.menuBar()
        overtime_menu = menu_bar.addMenu("잔업시간")
        # upload_menu = menu_bar.addMenu("업로드")
        
        select_all = QAction('전체 조회', self)
        select_all.setStatusTip("전체 조회")
        select_all.triggered.connect(self.select_all)

        select_dept = QAction('부서별 조회', self)
        select_dept.setStatusTip("부서별 조회")
        select_dept.triggered.connect(self.select_dept)

        upload_overtime = QAction('잔업시간 업로드', self)
        upload_overtime.setStatusTip("잔업시간 업로드")
        upload_overtime.triggered.connect(self.upload_overtime)

        overtime_menu.addAction(select_all)
        overtime_menu.addAction(select_dept)
        overtime_menu.addAction(upload_overtime)

        status_bar = self.statusBar()
        self.setStatusBar(status_bar)

    # def outgoing(self):
    #     print("new menu call")

    def select_all(self):
        import total_overtime as total_overtime_window

        self.total_window = total_overtime_window.MainWindow()
        self.total_window.show()
    
    def select_dept(self):
        import dept_overtime as select_dept_window

        self.dept_window = select_dept_window.DeptMainWindow()
        self.dept_window.show() 

    def upload_overtime(self):
        import upload as upload_window

        self.upload_window = upload_window.MainWindow()
        self.upload_window.show()

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