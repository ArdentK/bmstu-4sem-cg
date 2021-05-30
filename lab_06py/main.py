from timeit import timeit

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QLabel
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint

from mainwindow import Ui_MainWindow
from structures import Dot, Figure
from line_algos import dda
from canvas import DataTable
import sys


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui_setup()

    def ui_setup(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.QRB_figure.click()
        self.ui.canvas.image_init()
        self.ui.canvas.image_set()
        self.bind_buttons()
        self.ui.canvas.set_table(self.ui.QTW_table)
        self.ui.canvas.set_ui(self.ui)

    def bind_buttons(self):
        self.ui.QPB_add_dot.clicked.connect(lambda: self.change_mode())
        self.ui.QPB_clear.clicked.connect(lambda: self.clear())
        self.ui.QPB_lock.clicked.connect(lambda: self.ui.canvas.close_poly())

    def change_mode(self):
        if self.ui.QRB_figure.isChecked():
            self.add_dot_by_btn()
        if self.ui.QRB_seeding_point.isChecked():
            self.add_seed_by_btn()

    def add_dot_by_btn(self):
        dot = Dot(self.ui.QSB_x.value(), self.ui.QSB_y.value())
        self.ui.canvas.add_dot(dot)

    def add_seed_by_btn(self):
        dot = Dot(self.ui.QSB_x.value(), self.ui.QSB_y.value())
        self.ui.canvas.set_seeding_dot(dot)

    def clear(self):
        self.ui.canvas.clear()
        self.ui.QTW_table.clear()
        self.ui.QL_seed.setText("Затравочная точка:")

    def resizeEvent(self, event: QtGui.QResizeEvent):
        self.ui.canvas.image_init()
        self.ui.canvas.image_set()
        return super().resizeEvent(event)

    def time_info(self, time):
        if time is not None:
            text = f'Время закраски: {round(time, 2)} мс'
        else:
            text = f'Время закраски: None'
        QtWidgets.QMessageBox.about(self, "Время", text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    w = App()
    w.show()
    sys.exit(app.exec_())
