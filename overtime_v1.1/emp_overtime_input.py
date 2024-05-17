import os
import sys
# import warnings
# import time

import openpyxl
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from datetime import datetime
from openpyxl.styles import Alignment

# 절대경로를 상대경로로 변경 하는 함수
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#UI파일 연결
# main_window= uic.loadUiType(resource_path("/Users/black/projects/make_erp/main_window.ui"))[0] # Mac 사용시 ui 주소
emp_overtime_input_window= uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\overtime_v1.1\\ui\\emp_overtime_input.ui"))[0] # Window 사용시 ui 주소
dept_window = uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\overtime_v1.1\\ui\\dept_window.ui"))[0]
emp_window = uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\overtime_v1.1\\ui\\emp_window.ui"))[0]

# dial_window= uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\popup_dept_info.ui"))[0] # Window 사용시 ui 주소

#화면을 띄우는데 사용되는 Class 선언
class MainWindow(QWidget, emp_overtime_input_window) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("사원 잔업시간 입력")
        self.slots()
        # self.date_edit.setDate(QDate.currentDate())
        # self.date = self.date_edit.date().toString("yyyyMMdd")

    def slots(self):
        # self.btn_search.clicked.connect(self.make_data)
        self.btn_close.clicked.connect(self.window_close)
        self.btn_select_dept.clicked.connect(self.popup_dept_info)
        self.btn_select_emp.clicked.connect(self.popup_emp_info)
        self.btn_input.clicked.connect(self.input_data)
        self.btn_delete.clicked.connect(self.delete_rows)
        self.btn_save.clicked.connect(self.upload)
        # self.btn_clear.clicked.connect(self.clear)

    # def set_date(self):
    #     date = self.date_select.date()
    #     self.txt_date.setText(date.toString("yyyy-MM"))

    def clear(self):        
        self.tbl_info.setRowCount(0) # clear()는 행은 그대로 내용만 삭제, 행을 "0" 호출 한다.

        self.txt_dept_id.setText("")
        self.txt_dept_name.setText("")
        self.txt_emp_id.setText("")
        self.txt_emp_name.setText("")

    def input_data(self):

        overtime_date = self.date.date()
        overtime_date = overtime_date.toString("yyyy-MM-dd")

        dept_id = self.txt_dept_id.toPlainText()
        dept_name = self.txt_dept_name.toPlainText()
        emp_id = self.txt_emp_id.toPlainText()
        emp_name = self.txt_emp_name.toPlainText()
        overtime = self.txt_overtime.toPlainText()
        from_time = self.txt_from_time.toPlainText()
        to_time = self.txt_to_time.toPlainText()
        detail = self.txt_detail.toPlainText()
        note = self.txt_note.toPlainText()

        list = [dept_id, dept_name, emp_id, emp_name, overtime_date, from_time, to_time, str(overtime), detail, note]
        title = ["부서ID", "부서명", "사번", "사원명", "잔업일자", "잔업시간", "시작시간", "종료시간", "작업내용", "비고"]
        
        # 필수 입력값 
        list_must = [dept_id, dept_name, emp_id, emp_name, overtime_date, str(overtime)]
        title_must = ["부서ID", "부서명", "사번", "사원명", "잔업일자", "잔업시간"]

        # 필수 입력값 중 하나라도 ""이면 처리 중단
        for i, value in enumerate(list_must, start=1):
            if value == "":
                self.msg_box("입력오류", f"{title_must[i-1]} 값이 누락 됐습니다.")
                return

        row_count = self.tbl_info.rowCount()
        col_count = len(title)
        
        self.tbl_info.insertRow(row_count)
        self.tbl_info.setColumnCount(col_count)
        self.tbl_info.setHorizontalHeaderLabels(title)

        for i in range(col_count):
            self.tbl_info.setItem(row_count, i, QTableWidgetItem(str(list[i])))
            self.tbl_info.item(row_count, i).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

            self.txt_dept_id.setText("")
            self.txt_dept_name.setText("")
            self.txt_emp_id.setText("")
            self.txt_emp_name.setText("")
            self.txt_overtime.setText("")
            self.txt_from_time.setText("")
            self.txt_to_time.setText("")
            self.txt_detail.setText("")
            self.txt_note.setText("")
        
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

    def upload(self):
        # 현재 테이블 데이터(수정, 삭제 될 수 있다.)
        rows = self.tbl_info.rowCount()
        cols = self.tbl_info.columnCount()

        list = [] # 최종적으로 사용할 리스트는 for문 밖에 선언
        for i in range(rows):
            list_1 = []
            for j in range(cols):
                data = self.tbl_info.item(i,j)
                list_1.append(data.text())
            list.append(list_1)

        from db.db_insert import Insert
        data_insert = Insert()
        result = data_insert.insert_overtime(list)

        self.msg_box(result[0], result[1])
        self.tbl_info.setRowCount(0)

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
    def popup_emp_info(self):
        arg_1 = self.txt_dept_id.toPlainText()
        input_dialog = EmpWindow(arg_1) ##   <-----중요 포인트
        if input_dialog.exec_():
            value = input_dialog.get_input_value()

        try:
            self.txt_emp_id.setText(value[2].text())
            self.txt_emp_name.setText(value[3].text())
        except:
            return
        
    def get_dept_id(self):
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
                self.tbl_info.item(i, j).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  

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

class EmpWindow(QDialog, emp_window):
    def __init__(self, arg_1) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("사원선택")
        self.slots()

        self.dept_id = arg_1

        self.make_table()

    def slots(self):
        ### 다이알로그 시그널 생성기 반드시!!!!!!!! 필요. 없으면 작동 안 함############
        self.btn_confirm.clicked.connect(self.accept) # Close the dialog when OK is clicked 

    def make_table(self):
        from db.db_select import Select
        select = Select()
        select_emp = select.select_employee(self.dept_id)

        self.tbl_info.setRowCount(0) # clear()는 행은 그대로 내용만 삭제, 행을 "0" 호출 한다.

        if select_emp is None:
            num = 0
        else:
            num = len(select_emp)

        column_title = ["부서아이디", "부서명", "사원번호", "사원명"]
        col = len(column_title)

        self.tbl_info.setRowCount(num)
        self.tbl_info.setColumnCount(col)
        self.tbl_info.setHorizontalHeaderLabels(column_title)

        for i in range(num):
            for j in range(col): # 아니면 10개
                self.tbl_info.setItem(i, j, QTableWidgetItem(select_emp[i][j]))
                self.tbl_info.item(i, j).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)  

        # 컨텐츠의 길이에 맞추어 컬럼의 길이를 자동으로 조절
        ################################################################
        table = self.tbl_info
        # header = table.horizontalHeader()
        table.setColumnWidth(0, int(table.width() * 0.25))
        table.setColumnWidth(1, int(table.width() * 0.25))
        table.setColumnWidth(2, int(table.width() * 0.25))
        table.setColumnWidth(3, int(table.width() * 0.25))

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