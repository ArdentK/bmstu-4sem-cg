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
        self.ui.canvas.image_init()
        self.ui.canvas.image_set()
        self.bind_buttons()
        self.ui.canvas.set_table(self.ui.QTW_table)

    def bind_buttons(self):
        self.ui.QPB_clear.clicked.connect(lambda: self.clear())
        self.ui.QPB_lock.clicked.connect(lambda: self.ui.canvas.close_poly())
        self.ui.QPB_paint.clicked.connect(lambda: self.draw_rastor())

    def clear(self):
        self.ui.canvas.clear()
        self.ui.QTW_table.clear()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.ui.canvas.image_init()
        self.ui.canvas.image_set()
        return super().resizeEvent(event)

    def time_info(self, time):
        if time is not None:
            text = f'Время закраски: {round(time, 2)} мс'
        else:
            text = f'Время закраски: None'
        QtWidgets.QMessageBox.about(self, "Время", text)

    def get_curr_color(self):
        color_text = self.ui.QCB_color.currentText()

        if (color_text == "Белый(фон)"):
            color = Qt.white
        elif (color_text == "Черный"):
            color = Qt.black
        elif (color_text == "Красный"):
            color = Qt.red
        elif (color_text == "Синий"):
            color = Qt.blue

        return color

    def draw_rastor(self):
        color = self.get_curr_color()
        result = None
        if self.ui.QCB_delay.isChecked():
            self.ui.canvas.fill(color, True)
        else:
            result = timeit(lambda: self.ui.canvas.fill(color),
                            number=1) * 1000
            self.time_info(result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    w = App()
    w.show()
    sys.exit(app.exec_())
