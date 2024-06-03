import os
import sys
# import warnings
# import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QDate
from PyQt5 import uic, QtWidgets

# 절대경로를 상대경로로 변경 하는 함수
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#UI파일 연결
# main_window= uic.loadUiType(resource_path("/Users/black/projects/make_erp/main_window.ui"))[0] # Mac 사용시 ui 주소
emp_overtime_update_window= uic.loadUiType(resource_path("./ui/emp_overtime_update.ui"))[0] # Window 사용시 ui 주소
dept_window = uic.loadUiType(resource_path("./ui/dept_window.ui"))[0]
emp_window = uic.loadUiType(resource_path("./ui/emp_window.ui"))[0]

# dial_window= uic.loadUiType(resource_path("C:\\myproject\\python project\\overtime\\popup_dept_info.ui"))[0] # Window 사용시 ui 주소

#화면을 띄우는데 사용되는 Class 선언
class MainWindow(QWidget, emp_overtime_update_window) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("사원 잔업시간 수정")
        self.slots()
        self.date_from.setDate(QDate.currentDate())
        self.date_to.setDate(QDate.currentDate())
        # self.date = self.date_edit.date().toString("yyyyMMdd")
        self.setFixedSize(QSize(1079,823))

    def slots(self):
        # self.btn_search.clicked.connect(self.make_data)
        self.btn_close.clicked.connect(self.window_close)
        self.btn_select_dept.clicked.connect(self.popup_dept_info)
        self.btn_select_emp.clicked.connect(self.popup_emp_info)
        self.btn_select.clicked.connect(self.search_overtime_info)
        self.btn_delete.clicked.connect(self.delete_overtime_info)
        self.btn_update.clicked.connect(self.update_overtime_info)
        self.tbl_info.cellClicked.connect(self.select_info)
        # self.btn_save.clicked.connect(self.upload)
        # self.btn_input.clicked.connect(self.input_data)
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

    def search_overtime_info(self):
        date_from = self.date_from.date().toString("yyyy-MM-dd")
        date_to = self.date_to.date().toString("yyyy-MM-dd")

        dept_id = self.txt_dept_id.toPlainText()
        if dept_id == "":
            dept_id = '%%'
        else:
            dept_id

        emp_id = self.txt_emp_id.toPlainText()
        if emp_id == "":
            emp_id = '%%'
        else:
            emp_id

        arr = [date_from, date_to, dept_id, emp_id]

        from db.db_select import Select
        select = Select()
        result = select.update_overtime(arr)

        if result is None:
            return        
        else:
            title = ["ID", "부서아이디", "부서명", "사번", "이름", "날짜", "잔업시간", "시작시간", "종료시간", "작업내용", "비고"]
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

    def select_info(self):
        x = self.tbl_info.selectedIndexes() # 리스트로 선택된 행번호와 열번호가 x에 입력된다.
        row = x[0].row() #첫번째 선택된 행번호를 부르는 방법
        num_col = self.tbl_info.columnCount()

        list = []
        for i in range(num_col):
            value = self.tbl_info.item(row, i).text()
            list.append(value)

        date = list[5]
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])

        d = QDate(year, month, day)

        self.date_from.setDate(d)
        self.date_to.setDate(d)
        
        self.txt_id.setText(list[0])
        self.txt_dept_id.setText(list[1])
        self.txt_dept_name.setText(list[2])
        self.txt_emp_id.setText(list[3])
        self.txt_emp_name.setText(list[4])
        self.txt_overtime.setText(list[6])
        self.txt_from_time.setText(list[7])
        self.txt_to_time.setText(list[8])
        self.txt_detail.setText(list[9])
        self.txt_note.setText(list[10])

    def delete_overtime_info(self):
        id = self.txt_id.toPlainText()
        dept_name = self.txt_dept_name.toPlainText()
        emp_name = self.txt_emp_name.toPlainText()

        option = QtWidgets.QMessageBox.question(self, "QMessageBox", f"{dept_name} {emp_name} 사원의 잔업정보를 삭제 하시겠습니까?", 
                                       QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Yes)
        
        if option == QtWidgets.QMessageBox.Cancel:
            return
        elif option == QtWidgets.QMessageBox.No:
            return
        elif option == QtWidgets.QMessageBox.Yes: 

            from db.db_delete import Delete
            delete = Delete()
            delete.delete_emp_overtime(id)
            self.tbl_info.setRowCount(0)

    def update_overtime_info(self):
        now = QDate.currentDate()
        date_from = self.date_from.date()
        days = date_from.daysTo(now)

        if days > 30:
            self.msg_box("수정오류", "수정 가능 기간이 지났습니다.")
            return
        else:
            id = self.txt_id.toPlainText()
            dept_name = self.txt_dept_name.toPlainText()
            emp_name = self.txt_emp_name.toPlainText()

            overtime = self.txt_overtime.toPlainText()
            from_time = self.txt_from_time.toPlainText()
            to_time = self.txt_to_time.toPlainText()
            detail = self.txt_detail.toPlainText()
            note = self.txt_note.toPlainText()

            update_list = [overtime, from_time, to_time, detail, note, id]

            option = QtWidgets.QMessageBox.question(self, "QMessageBox", f"{dept_name} {emp_name} 사원의 잔업정보를 수정 하시겠습니까?", 
                                        QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Yes)
            
            if option == QtWidgets.QMessageBox.Cancel:
                return
            elif option == QtWidgets.QMessageBox.No:
                return
            elif option == QtWidgets.QMessageBox.Yes: 

                from db.db_update import Update
                update = Update()
                update.update_emp_overtime(update_list)
                self.tbl_info.setRowCount(0)

                self.date_from.setDate(QDate.currentDate())
                self.date_to.setDate(QDate.currentDate())

                self.txt_dept_id.setText("")
                self.txt_dept_name.setText("")
                self.txt_emp_id.setText("")
                self.txt_emp_name.setText("")
                self.txt_overtime.setText("")
                self.txt_from_time.setText("")
                self.txt_to_time.setText("")
                self.txt_detail.setText("")
                self.txt_note.setText("")

                from db.db_select import Select
                select = Select()
                result = select.update_overtime_id(id)

                title = ["ID", "부서아이디", "부서명", "사번", "이름", "날짜", "잔업시간", "시작시간", "종료시간", "작업내용", "비고"]
                self.make_table(len(result), result, title)

    def delete_overtime_info(self):
        now = QDate.currentDate()
        date_from = self.date_from.date()
        days = date_from.daysTo(now)

        if days > 30:
            self.msg_box("삭제오류", "삭제 가능 기간이 지났습니다.")
            return
        else:
            id = self.txt_id.toPlainText()
            dept_name = self.txt_dept_name.toPlainText()
            emp_name = self.txt_emp_name.toPlainText()

            option = QtWidgets.QMessageBox.question(self, "QMessageBox", f"{dept_name} {emp_name} 사원의 잔업정보를 삭제 하시겠습니까?", 
                                        QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Yes)
            
            if option == QtWidgets.QMessageBox.Cancel:
                return
            elif option == QtWidgets.QMessageBox.No:
                return
            elif option == QtWidgets.QMessageBox.Yes: 

                from db.db_delete import Delete
                delete = Delete()
                delete.delete_emp_overtime(id)
                self.tbl_info.setRowCount(0)               
                
                self.search_overtime_info()

                self.date_from.setDate(QDate.currentDate())
                self.date_to.setDate(QDate.currentDate())

                self.txt_dept_id.setText("")
                self.txt_dept_name.setText("")
                self.txt_emp_id.setText("")
                self.txt_emp_name.setText("")
                self.txt_overtime.setText("")
                self.txt_from_time.setText("")
                self.txt_to_time.setText("")
                self.txt_detail.setText("")
                self.txt_note.setText("")

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

        list = [dept_id, dept_name, emp_id, emp_name, overtime_date, str(overtime), from_time, to_time, detail, note]
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
        self.tbl_info.cellDoubleClicked.connect(self.accept)

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
        self.tbl_info.cellDoubleClicked.connect(self.accept)

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