import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from datetime import datetime
import pymysql

class TemperatureChart(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Overtime")
        self.setGeometry(100, 100, 800, 600)
        self.db_select()

    def db_select(self):
        # doochpump 화성공장 hr server 
        self.host = "106.248.19.234"
        self.port = 3306
        self.database = "webserver"
        self.username = "scott"
        self.password = "!Jhlee0809" 

        self.conn = pymysql.connect(host=self.host, user=self.username, passwd=self.password, db=self.database, port=self.port, use_unicode=True, charset='utf8')
        cursor = self.conn.cursor()

        try:
            query = """SELECT
                        dept_name,
                        SUM(CASE WHEN yyyy_mm = '2024-01' THEN overtime ELSE 0 END) AS '2024-01',
                        SUM(CASE WHEN yyyy_mm = '2024-02' THEN overtime ELSE 0 END) AS '2024-02',
                        SUM(CASE WHEN yyyy_mm = '2024-03' THEN overtime ELSE 0 END) AS '2024-03',
                        SUM(CASE WHEN yyyy_mm = '2024-04' THEN overtime ELSE 0 END) AS '2024-04',
                        SUM(CASE WHEN yyyy_mm = '2024-05' THEN overtime ELSE 0 END) AS '2024-05',
                        SUM(CASE WHEN yyyy_mm = '2024-06' THEN overtime ELSE 0 END) AS '2024-06',
                        SUM(CASE WHEN yyyy_mm = '2024-07' THEN overtime ELSE 0 END) AS '2024-07',
                        SUM(CASE WHEN yyyy_mm = '2024-08' THEN overtime ELSE 0 END) AS '2024-08',
                        SUM(CASE WHEN yyyy_mm = '2024-09' THEN overtime ELSE 0 END) AS '2024-09',
                        SUM(CASE WHEN yyyy_mm = '2024-10' THEN overtime ELSE 0 END) AS '2024-10',
                        SUM(CASE WHEN yyyy_mm = '2024-11' THEN overtime ELSE 0 END) AS '2024-11',
                        SUM(CASE WHEN yyyy_mm = '2024-12' THEN overtime ELSE 0 END) AS '2024-12'
                    FROM (    
                            SELECT * FROM overtime_test
                        ) T
                    GROUP BY dept_name;"""
            cursor.execute(query) #excute 문에 조회용 변수를 전달 할 때는 튜블 또는 리스트로 !!!!
            result = cursor.fetchall()
            self.make_data(result)

        except Exception as e:
            # self.msg_box("Error", str(e))
            return

    def make_data(self, result):
        rows = len(result)

        dept_name = []
        for i in result:
            dept_name.append(i[0])

        for i in range(rows):
            globals()['data_' + str(i)] = []
            for j in result:
                globals()['data_' + str(i)].append(j)

        print('sss')

        # 부서명
        self.dept = ["SCM-자재", "생산팀_1파트", "생산팀_2파트", "생산팀_3파트", "생산팀_4파트"]

        # # Example monthly average temperature data for 3 cities
        self.months = ["2004/01", "2004/02", "2004/03", "2004/04", "2004/05", "2004/06", "2004/07", "2004/08", "2004/09", "2004/10", "2004/11", "2004/12"]
        self.dept_1 = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.dept_2 = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.dept_3 = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.dept_4 = [0,0,0,0,0,0,0,0,0,0,0,0]

        # # Create bar sets for each city
        self.bar_set_city1 = QBarSet("SCM-자재")
        self.bar_set_city1.append(self.dept_1)

        self.bar_set_city2 = QBarSet("생산팀_1파트")
        self.bar_set_city2.append(self.dept_2)

        self.bar_set_city3 = QBarSet("생산팀_2파트")
        self.bar_set_city3.append(self.dept_3)
        
        self.bar_set_city4 = QBarSet("생산팀_3파트")
        self.bar_set_city4.append(self.dept_4)

        self.bar_set_city5 = QBarSet("생산팀_4파트")
        self.bar_set_city5.append(self.dept_5)

        # # Create the bar series and add the bar sets
        self.bar_series = QBarSeries()
        self.bar_series.append(self.bar_set_city1)
        self.bar_series.append(self.bar_set_city2)
        self.bar_series.append(self.bar_set_city3)
        self.bar_series.append(self.bar_set_city4)
        self.bar_series.append(self.bar_set_city5)

        # Create the chart and add the series
        self.chart = QChart()
        self.chart.addSeries(self.bar_series)
        self.chart.setTitle("Overtime")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # Create the X axis and set the categories (months)
        self.axisX = QBarCategoryAxis()
        self.axisX.append(self.months)
        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.bar_series.attachAxis(self.axisX)

        # Create the Y axis and set the range
        self.axisY = QValueAxis()
        self.axisY.setRange(0, 35)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)
        self.bar_series.attachAxis(self.axisY)

        # Create the chart view and set the chart
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Set the central widget and layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.chart_view)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TemperatureChart()
    window.show()
    sys.exit(app.exec_())