import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from PyQt5 import uic, QtWidgets
import openpyxl
from openpyxl.styles import Alignment
from datetime import datetime
# 차트 생성용
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 절대경로를 상대경로로 변경 하는 함수
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# matplotlib 폰트 설정
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

#UI파일 연결
# main_window= uic.loadUiType(resource_path("/Users/black/projects/make_erp/main_window.ui"))[0] # Mac 사용시 ui 주소
main_window= uic.loadUiType(resource_path("./ui/main_window.ui"))[0] # Window 사용시 ui 주소

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, main_window) :
    def __init__(self) :
        super().__init__()

        self.version = 1.4

        from db.db_select import Select
        select = Select()
        result = select.select_version()

        if self.version == result[0][0]:
            self.setupUi(self)
            self.setWindowTitle("DOOCH PUMP HR")
            self.setFixedSize(QSize(1337,839)) # 해상도에 따라 구성 비율이 변경되게 하고 싶지 않은 경우 창의 크기를 고정 시킨다.
            self.check_login()
        else:
            self.msg_box("확인", "사용중인 프로그램의 버전 확인이 필요합니다.")
            return
        
        self.slots()

    def slots(self):
        self.btn_refresh.clicked.connect(self.refresh_report)
        self.btn_download.clicked.connect(self.make_file)

    def check_login(self): 
        text, ok = QInputDialog.getText(self, 'Input Dialog', '사용자 번호 :')
        if ok:
            id = self.version
            password = text
        else:
            self.setFixedSize(QSize(0,0))
            return

        from db.db_select import Select
        select = Select()
        result = select.select_password(id)

        if password == result[0]:
            self.btn_refresh.show()
            self.btn_download.show()

            self.mainwindow()
        else:
            self.msg_box("오류", "사용자 코드를 확인 하세요.")
            self.setFixedSize(QSize(0,0))
            return


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

        self.monthly_dept_report()
        self.monthly_sum_report()

    def make_chart(self, column_name, result):
        fig = plt.Figure()
        self.canvas = FigureCanvas(fig)
        self.layout_chart.addWidget(self.canvas)

        year_month = column_name[1:13]
        overtime = result[0][1:13]

        self.ax = fig.add_subplot(111)
        self.bars = self.ax.bar(year_month, overtime)
        self.ax.set_title('Bar Chart')
        self.canvas.draw()

        self.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.inaxes == self.ax and self.bars is not None:
            for bar in self.bars:
                if bar.contains(event)[0]:
                    label = bar.get_x() + bar.get_width() / 2
                    value = bar.get_height()
                    self.show_pie_chart(label, value)
                    break

    def show_pie_chart(self, label, value):
        fig = plt.Figure()
        canvas = FigureCanvas(fig)
        self.layout_chart.addWidget(canvas)

        ax = fig.add_subplot(111)
        other_values = sum(bar.get_height() for bar in self.bars) - value
        ax.pie([value, other_values], labels=[f'{label}: {value}', f'Others: {other_values}'], autopct='%1.1f%%')
        ax.set_title(f'Pie Chart for {label}')
        canvas.draw()

    def refresh_report(self):
        option = QtWidgets.QMessageBox.question(self, "QMessageBox", f"잔업 정보를 새로고침 하시겠습니까?", 
                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
            
        if option == QtWidgets.QMessageBox.Cancel:
            return
        elif option == QtWidgets.QMessageBox.No:
            return
        elif option == QtWidgets.QMessageBox.Yes: 
            self.monthly_dept_report()
            self.monthly_sum_report()

    def monthly_dept_report(self):
        self.lbl_dept.show()
        self.tbl_dept_info.show()
        
        from db.db_select import Select
        select = Select()
        result, column_names = select.select_dept_monthly()

        self.make_dept_table(len(result), result, column_names)
        self.make_chart(column_names, result)

    def monthly_sum_report(self):
        self.tbl_month_info.show()
        
        from db.db_select import Select
        select = Select()
        result, column_names = select.select_monthly_sum()

        self.make_sum_table(len(result), result, column_names)
        self.make_chart(column_names, result)

    def make_dept_table(self, num, arr_1, column_names):   
        self.tbl_dept_info.setRowCount(0)

        col = len(column_names)

        self.tbl_dept_info.setRowCount(num)
        self.tbl_dept_info.setColumnCount(col)
        self.tbl_dept_info.setHorizontalHeaderLabels(column_names)

        for i in range(num):
            for j in range(col): 
                self.tbl_dept_info.setItem(i, j, QTableWidgetItem(str(arr_1[i][j])))
                self.tbl_dept_info.item(i, j).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)     

        table = self.tbl_dept_info
        header = table.horizontalHeader()

        for i in range(col):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.tbl_dept_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def make_sum_table(self, num, arr_1, column_names):   
        self.tbl_month_info.setRowCount(0)

        col = len(column_names)

        self.tbl_month_info.setRowCount(num)
        self.tbl_month_info.setColumnCount(col)

        for i in range(num):
            for j in range(col):
                self.tbl_month_info.setItem(i, j, QTableWidgetItem(str(arr_1[i][j])))
                self.tbl_month_info.item(i, j).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)     

        table = self.tbl_month_info
        header = table.horizontalHeader()
        header.hide()

        for i in range(col):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.tbl_month_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def make_file(self):
        rows_dept_table = self.tbl_dept_info.rowCount()
        cols_dept_table = self.tbl_dept_info.columnCount()

        list_dept_1 = []
        for i in range(rows_dept_table):
            list_dept_2 = []
            for j in range(cols_dept_table):
                try:
                    list_dept_2.append(self.tbl_dept_info.item(i,j).text())
                except:
                    list_dept_2.append('')
            list_dept_1.append(list_dept_2)

        rows_month_table = self.tbl_month_info.rowCount()
        cols_month_table = self.tbl_month_info.columnCount()

        list_month_1 = []
        for i in range(rows_month_table):
            list_month_2 = []
            for j in range(cols_month_table):
                try:
                    list_month_2.append(self.tbl_month_info.item(i,j).text())
                except:
                    list_month_2.append('')
            list_month_1.append(list_month_2)

        time = datetime.now()
        time_str = time.strftime("%Y%m%d_%H%M%S")

        file_name = f"부서별_월별_잔업현황_{time_str}.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active

        ws.append(['부서별 월간 잔업 현황'])

        for data in list_dept_1:
            ws.append(data)
        ws.append([''])
        ws.append([''])
        ws.append([''])

        ws.append(['월간 총 잔업 현황'])

        for data in list_month_1:
            ws.append(data)
        ws.append([''])

        for rows in ws.iter_rows():
            for cell in rows:
                cell.alignment = Alignment(horizontal='center', vertical='center')

        wb.save(file_name)
        self.msg_box('다운로드', f'{file_name} 파일이 생성되었습니다.')

    def msg_box(self, title, content):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(content)
        msg.exec_()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
