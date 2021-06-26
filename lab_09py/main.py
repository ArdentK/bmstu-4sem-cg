from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QLabel
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint

from mainwindow import Ui_MainWindow
import sys


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui_setup()

    def ui_setup(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.QRB_polygon.click()
        self.ui.canvas.set_ui(self.ui)
        self.bind_buttons()

    def bind_buttons(self):
        self.ui.QPB_clear.clicked.connect(lambda: self.clear())
        self.ui.QPB_cut.clicked.connect(
            lambda: self.ui.canvas.cut_polygon())

    def clear(self):
        self.ui.canvas.clear()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        self.ui.canvas.image_init()
        self.ui.canvas.image_set()
        return super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    w = App()
    w.show()
    sys.exit(app.exec_())
