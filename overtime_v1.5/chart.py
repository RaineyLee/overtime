import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# 월별 평균 강수량 데이터 (예시 데이터)
months = ['1mon', '2mon', '3mon', '4mon', '5mon', '6mon', '7mon', '8mon', '9mon', '10mon', '11mon', '12mon']
precipitation = [50.3, 40.2, 55.7, 78.8, 90.5, 110.3, 150.6, 140.2, 120.5, 85.4, 65.3, 50.9]

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

        self.plot()

    def plot(self):
        self.axes.bar(months, precipitation, color='green')
        self.axes.set_title('month mm')
        self.axes.set_xlabel('month')
        self.axes.set_ylabel('mm')

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("월별 평균 강수량 차트")
        self.setGeometry(100, 100, 800, 600)

        sc = MplCanvas(self, width=10, height=4, dpi=100)

        layout = QVBoxLayout()
        layout.addWidget(sc)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()