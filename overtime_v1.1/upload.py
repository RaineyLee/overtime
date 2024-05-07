import os
import sys
# import warnings
# import time

from openpyxl import *
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
main_window= uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\overtime_v1.1\\ui\\upload.ui"))[0] # Window 사용시 ui 주소

# dial_window= uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\popup_dept_info.ui"))[0] # Window 사용시 ui 주소

#화면을 띄우는데 사용되는 Class 선언
class MainWindow(QWidget, main_window) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("잔업시간 업로드")
        self.slots()

        # self.date_edit.setDate(QDate.currentDate())
        # self.date = self.date_edit.date().toString("yyyyMMdd")

    def slots(self):
        # self.date_edit.dateChanged.connect(self.set_date)
        self.btn_open.clicked.connect(self.file_open)
        self.btn_select.clicked.connect(self.make_data)
        self.btn_upload.clicked.connect(self.upload)
        self.btn_close.clicked.connect(self.window_close)
        self.btn_delete.clicked.connect(self.delete_rows)
        # self.btn_select_dept.clicked.connect(self.popup_dept_info)

    # def set_date(self):
    #     self.date = self.date_edit.date().toString("yyyyMMdd")

    def file_open(self):
        fname = QFileDialog.getOpenFileName(parent=self, caption='Open file', directory='C:.excel/')

        if fname[0]:
            self.text_select_file.setText(fname[0])
        else:
            self.text_select_file.setText("")
            QMessageBox.about(self, 'Warning', '파일을 선택하지 않았습니다.')

    def make_data(self):
        file_name = self.text_select_file.toPlainText()
        if file_name == "":
            return
        else:
            self.tbl_info.setRowCount(0) # clear()는 행은 그대로 내용만 삭제, 행을 "0" 호출 한다.
            file_name = self.text_select_file.toPlainText()

            from utils.make_data import Overtime
            make_data = Overtime(file_name)

            _list = make_data.excel_data()

            title = _list[1]
            data = _list[0]
                    
            self.make_table(len(data), data, title)

    def make_table(self, num, arr_1, arg_1):   
        col = len(arg_1)

        self.tbl_info.setRowCount(num)
        self.tbl_info.setColumnCount(col)
        self.tbl_info.setHorizontalHeaderLabels(arg_1)

        for i in range(num):
            for j in range(col): # 아니면 10개
                self.tbl_info.setItem(i, j, QTableWidgetItem(arr_1[i][j]))

        # 컨텐츠의 길이에 맞추어 컬럼의 길이를 자동으로 조절
        ################################################################
        table = self.tbl_info
        header = table.horizontalHeader()

        for i in range(col):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        ################################################################

        # 테이블의 길이에 맞추어 컬럼 길이를 균등하게 확장
        # self.tbl_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
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
        self.text_select_file.setText("")
        self.tbl_info.setColumnCount(0)
        self.tbl_info.setRowCount(0)

    # # 부서명 가져오기 팝업
    # def popup_dept_info(self):
    #     input_dialog = InputWindow()
    #     if input_dialog.exec_():
    #         value = input_dialog.get_input_value()

    #     try:
    #         self.txt_dept_id.setText(value[0].text())
    #         self.txt_dept_name.setText(value[1].text())
    #     except:
    #         return
        
    # def dept_name(self, arg_1):  
    #     self.txt_dept_id.setText("arg_1.text()")
    #     print(arg_1)

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