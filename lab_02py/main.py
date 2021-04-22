import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QGraphicsScene, QGraphicsView, QTableWidgetItem
from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtCore import Qt
import lab_02
from math import sin, cos, pi, radians
import numpy as np
import copy

start_x_center = 0
start_y_center = 0

pre_x_center = 0
pre_y_center = 0

x_center = 0
y_center = 0

a = 2
b = 3

dots = []
pre_dots = []


class App(QtWidgets.QMainWindow, lab_02.Ui_MainWindow):

    shift = 150

    def __init__(self):
        super(App, self).__init__()
        self.ui = lab_02.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_to_scale.clicked.connect(self.to_scale)
        self.ui.btn_to_transfer.clicked.connect(self.to_transfer)
        self.ui.btn_to_turn.clicked.connect(self.to_turn)
        self.ui.btn_to_restore.clicked.connect(self.to_restore)
        self.ui.btn_step_back.clicked.connect(self.step_back)

        self.createGraphicView()

    def createGraphicView(self):
        global dots, start_y_center, start_x_center, x_center, y_center, pre_y_center, pre_x_center

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()

        self.ui.graphicsView.setSceneRect(0, 0, 1, 1)
        self.ui.graphicsView.setAlignment(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.redBrush = QBrush(Qt.red)
        self.blackBrush = QBrush(Qt.black)

        self.redpen = QPen(Qt.red, 4)
        self.redpen3 = QPen(Qt.red, 1)
        self.greenpen2 = QPen(Qt.green, 2)
        self.blackpen = QPen(Qt.black, 4)
        self.bluepen = QPen(Qt.blue, 3)
        self.graypen = QPen(Qt.gray, 3)

        start_x_center = x_center = pre_x_center = width/2
        start_y_center = y_center = pre_y_center = height/2

        self.create_dots()

        self.shapes()

    def create_dots(self):
        global dots

        dots.clear()

        t = np.arange(0, 5*pi, pi/1000)

        for angle in t:
            x = (a + b) * cos(angle) - a * cos((a + b)*angle/a)
            y = (a + b) * sin(angle) - a * sin((a + b)*angle/a)

            dots.append({"x": x * 15, "y": y * 15})

        t = np.arange(-130, 130, 0.1)
        for i in range(len(t)):
            x = t[i]
            y = -110
            dots.append({"x": x, "y": y})
            y = 110
            dots.append({"x": x, "y": y})

        t = np.arange(-110, 110, 0.1)
        for i in range(len(t)):
            y = t[i]
            x = -130
            dots.append({"x": x, "y": y})
            x = 130
            dots.append({"x": x, "y": y})

    def shapes(self):
        global dots

        self.scene.clear()

        self.scene.addEllipse(
            x_center - 0.5, y_center - 0.5, 1, 1, self.blackpen, self.blackBrush)

        for i in range(len(dots)):
            self.scene.addEllipse(
                x_center + dots[i]["x"] - 1, y_center + dots[i]["y"] - 1, 2, 2, self.redpen3, self.redBrush)

    def to_scale(self):
        global x_center, y_center, dots, pre_dots, pre_x_center, pre_y_center

        _x_center = self.ui.x_center.text()
        _y_center = self.ui.y_center.text()
        _x_scaling_factor = self.ui.x_scaling_factor.text()
        _y_scaling_factor = self.ui.y_scaling_factor.text()

        try:
            _x_center = float(_x_center)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Координата по оси Х должна быть числом!")
            return

        try:
            _y_center = float(_y_center)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Координата по оси Y должна быть числом!")
            return

        try:
            _x_scaling_factor = float(_x_scaling_factor)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Коэффициент масштабирования по оси Х должен быть числом!")
            return

        try:
            _y_scaling_factor = float(_y_scaling_factor)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Коэффициент масштабирования по оси Y должен быть числом!")
            return

        pre_x_center = x_center
        pre_y_center = y_center
        pre_dots.clear()
        pre_dots = copy.deepcopy(dots)

        for i in range(len(dots)):
            dots[i]["x"] = (dots[i]["x"] + x_center -
                            _x_center) * _x_scaling_factor
            dots[i]["y"] = (dots[i]["y"] + y_center -
                            _y_center) * _y_scaling_factor

        x_center = _x_center
        y_center = _y_center

        self.shapes()

    def to_restore(self):
        global dots, x_center, y_center, start_y_center, start_x_center, pre_dots, pre_x_center, pre_y_center

        pre_dots.clear()
        pre_dots = copy.copy(dots)
        pre_x_center = x_center
        pre_y_center = y_center

        x_center = start_x_center
        y_center = start_y_center

        self.create_dots()
        self.shapes()

    def step_back(self):
        global x_center, y_center, pre_x_center, pre_y_center, dots, pre_dots

        if (len(pre_dots) == 0):
            QMessageBox.critical(
                self, "Ошибка", "Вернуться на шаг назад можно только 1 раз!")
            return

        dots.clear()
        dots = copy.deepcopy(pre_dots)
        x_center = pre_x_center
        y_center = pre_y_center

        pre_dots.clear()

        self.shapes()

    def to_transfer(self):
        global x_center, y_center, pre_x_center, pre_y_center, dots, pre_dots

        pre_dots = copy.deepcopy(dots)
        pre_x_center = x_center
        pre_y_center = y_center

        dx = self.ui.x_transfer_factor.text()
        dy = self.ui.y_transfer_factor.text()
        _x_center = self.ui.x_center.text()
        _y_center = self.ui.x_center.text()

        try:
            _x_center = float(_x_center)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Координата по оси Х должна быть числом!")
            return

        try:
            _y_center = float(_y_center)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Координата по оси Y должна быть числом!")
            return

        try:
            dx = float(dx)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Перенос по оси Х должна быть числом!")
            return

        try:
            dy = float(dy)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Перенос по оси Y должна быть числом!")
            return

        self.transfer_dots(dx, dy)

        self.shapes()

    def transfer_dots(self, _dx, _dy):
        global dots

        for i in range(len(dots)):
            dots[i]["x"] += _dx
            dots[i]["y"] += _dy

    def to_turn(self):
        global x_center, y_center, pre_x_center, pre_y_center, dots, pre_dots

        pre_dots = copy.deepcopy(dots)
        pre_x_center = x_center
        pre_y_center = y_center

        _x_center = self.ui.x_center.text()
        _y_center = self.ui.y_center.text()
        angle = self.ui.turn_angle.text()

        try:
            _x_center = float(_x_center)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Координата по оси Х должна быть числом!")
            return

        try:
            _y_center = float(_y_center)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Координата по оси Y должна быть числом!")
            return

        try:
            angle = float(angle)
        except ValueError:
            QMessageBox.critical(
                self, "Ошибка", "Угол должен быть числом!")
            return

        angle = -radians(angle)

        for i in range(len(dots)):
            new_x = (dots[i]["x"] + x_center - _x_center) * \
                cos(angle) - (dots[i]["y"] + y_center - _y_center) * sin(angle)
            dots[i]["y"] = (dots[i]["x"] + x_center - _x_center) * \
                sin(angle) + (dots[i]["y"] + y_center - _y_center) * cos(angle)
            dots[i]["x"] = new_x

        x_center = _x_center
        y_center = _y_center

        self.shapes()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
