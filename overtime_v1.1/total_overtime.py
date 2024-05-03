import os
import sys
# import warnings
# import time

from openpyxl import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate #Alignment 
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
total_overtime= uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\overtime_v1.1\\ui\\total_overtime.ui"))[0] # Window 사용시 ui 주소
dept_window = uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\overtime_v1.1\\ui\\dept_window.ui"))[0]
# emp_window = uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\overtime_v1.1\\ui\\emp_window.ui"))[0]

# dial_window= uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\popup_dept_info.ui"))[0] # Window 사용시 ui 주소

#화면을 띄우는데 사용되는 Class 선언
class MainWindow(QWidget, total_overtime) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("잔업시간 조회")
        self.slots()
        self.date_select.setDate(QDate.currentDate())
        
    def slots(self):
        self.btn_search.clicked.connect(self.make_data)
        # self.btn_close.clicked.connect(self.window_close)
        self.btn_search_dept.clicked.connect(self.popup_dept_info)
        # self.btn_select_emp.clicked.connect(self.popup_emp_info)
        self.btn_clear.clicked.connect(self.clear)

    # def set_date(self):
    #     date = self.date_select.date()
    #     self.txt_date.setText(date.toString("yyyy-MM"))

    def clear(self):        
        self.tbl_info.setRowCount(0) # clear()는 행은 그대로 내용만 삭제, 행을 "0" 호출 한다.

        self.txt_dept_id.setText("")
        self.txt_dept_name.setText("")
        self.txt_emp_id.setText("")
        self.txt_emp_name.setText("")

    def make_data(self):
        dept_id = self.txt_dept_id.toPlainText()
        date_1 = self.date_select.date().toString("yyyy-MM")

        if  dept_id:
            arr_1 = [dept_id, date_1, date_1]
           
            from db.db_select import Select
            select = Select()

            result = select.all_overtime_1(arr_1)

            title = ["부서아이디", "부서명", "사번", "이름", "날짜", "잔업시간", "시작시간", "종료시간", "작업내용", "비고"]
            self.make_table(len(result), result, title)
        elif dept_id == "":
            arr_1 = [date_1, date_1]
           
            from db.db_select import Select
            select = Select()

            result = select.all_overtime_2(arr_1)

            title = ["부서아이디", "부서명", "사번", "이름", "날짜", "잔업시간", "시작시간", "종료시간", "작업내용", "비고"]
            self.make_table(len(result), result, title)

    def make_table(self, num, arr_1, title):   
        self.tbl_info.setRowCount(0) # clear()는 행은 그대로 내용만 삭제, 행을 "0" 호출 한다.

        col = len(title)

        self.tbl_info.setRowCount(num)
        self.tbl_info.setColumnCount(col)
        self.tbl_info.setHorizontalHeaderLabels(title)

        for i in range(num):
            for j in range(col): # 아니면 10개
                self.tbl_info.setItem(i, j, QTableWidgetItem(str(arr_1[i][j])))
                self.tbl_info.item(i, j).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)     

        # 컨텐츠의 길이에 맞추어 컬럼의 길이를 자동으로 조절
        ################################################################
        table = self.tbl_info
        header = table.horizontalHeader()

        for i in range(col):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        ################################################################

        # 테이블의 길이에 맞추어 컬럼 길이를 균등하게 확장
        self.tbl_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    # 테이블 선택범위 삭제
    def delete_rows(self):
        indexes = []
        rows = []

        for idx in self.tbl_info.selectedItems():
            indexes.append(idx.row())

        for value in indexes:
            if value not in rows:
                rows.append(value)

        # 삭제시 오류 방지를 위해 아래서 부터 삭제(리버스 소팅)
        rows = sorted(rows, reverse=True)

        # 선택행 삭제
        for rowid in rows:
            self.tbl_info.removeRow(rowid)

    # 부서명 가져오기 팝업
    def popup_dept_info(self):
        input_dialog = DeptWindow()
        if input_dialog.exec_():
            value = input_dialog.get_input_value()

            try:
                self.txt_dept_id.setText(value[0].text())
                self.txt_dept_name.setText(value[1].text())
            except:
                return
        
    ### 다이알로그 창으로 값을 전달 할 때는 아규먼트를 보내 주는 방식으로 !!!!
    # def popup_emp_info(self):
    #     arg_1 = self.txt_dept_id.toPlainText()
    #     input_dialog = EmpWindow(arg_1) ##   <-----중요 포인트
    #     if input_dialog.exec_():
    #         value = input_dialog.get_input_value()

    #     try:
    #         self.txt_emp_id.setText(value[2].text())
    #         self.txt_emp_name.setText(value[3].text())
    #     except:
    #         return
        
    def get_dept_id(self):
        print(self.dept_id)
        return self.dept_id


    def msg_box(self, arg_1, arg_2):
        msg = QMessageBox()
        msg.setWindowTitle(arg_1)               # 제목설정
        msg.setText(arg_2)                          # 내용설정
        msg.exec_()                                 # 메세지박스 실행

    def window_close(self):
        self.close()


class DeptWindow(QDialog, dept_window):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("부서선택")
        self.slots()

        self.make_table()

    def slots(self):
        ### 다이알로그 시그널 생성기 반드시!!!!!!!! 필요. 없으면 작동 안 함############
        self.btn_confirm.clicked.connect(self.accept) # Close the dialog when OK is clicked 

    def make_table(self):
        from db.db_select import Select
        select = Select()
        select_dept = select.select_department()

        self.tbl_info.setRowCount(0) # clear()는 행은 그대로 내용만 삭제, 행을 "0" 호출 한다.

        if select_dept is None:
            num = 0
        else:
            num = len(select_dept)
        col = self.tbl_info.columnCount()

        self.tbl_info.setRowCount(num)
        self.tbl_info.setColumnCount(col)
        # self.tbl_info.setHorizontalHeaderLabels(column_title)

        for i in range(num):
            for j in range(col): # 아니면 10개
                self.tbl_info.setItem(i, j, QTableWidgetItem(select_dept[i][j]))

        # 컨텐츠의 길이에 맞추어 컬럼의 길이를 자동으로 조절
        ################################################################
        table = self.tbl_info
        # header = table.horizontalHeader()
        table.setColumnWidth(0, int(table.width() * 0.5))
        table.setColumnWidth(1, int(table.width() * 0.5))

        # for i in range(col):
        #     header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        ################################################################

        # 테이블의 길이에 맞추어 컬럼 길이를 균등하게 확장
        self.tbl_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def get_input_value(self):
        list = self.tbl_info.selectedItems()
        return list

    def msg_box(self, arg_1, arg_2):
        msg = QMessageBox()
        msg.setWindowTitle(arg_1)               # 제목설정
        msg.setText(arg_2)                          # 내용설정
        msg.exec_()                                 # 메세지박스 실행

    def window_close(self):
        self.close()



if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()