import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QGraphicsScene, QGraphicsView, QTableWidgetItem
from PyQt5.QtGui import QBrush, QPen, QPainter, QColor
from PyQt5.QtCore import Qt
import design
from math import *
import numpy as np
import time
import matplotlib.pyplot as plt

eps = 1e-5


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super(App, self).__init__()
        self.ui = design.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.QCBox_color.activated.connect(self.set_current_color)
        self.ui.QCBox_method.activated.connect(self.set_current_method)

        self.ui.btn_to_clear.clicked.connect(self.to_clear)
        self.ui.btn_to_draw_line.clicked.connect(self.draw_line)
        self.ui.btn_to_draw_spectrum.clicked.connect(self.draw_spectrum)
        self.ui.btn_to_output_efficiency.clicked.connect(self.analysys_time)
        self.ui.btn_to_output_gradation.clicked.connect(self.analysys_stepping)

        self.createGraphicView()

    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()

        self.ui.graphicsView.setSceneRect(0, 0, width-10, height-10)
        self.ui.graphicsView.setAlignment(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.pen = QPen(Qt.white, 1)

        self.ui.QDSB_x_spectrum.setValue(width/2)
        self.ui.QDSB_y_spectrum.setValue(height/2)
        self.ui.QDSB_angle_step.setValue(10)
        self.ui.QDSB_radius.setValue(250)

        self.line_coordinates = [0, 0, 1, 1]
        self.spectrum_params = [0, 0]
        self.spectrum_center = [width / 2, height / 2]
        self.set_current_color()
        self.set_current_method()

    def draw_line(self):
        self.get_line_coordinates()
        self.set_current_color()
        self.set_current_method()
        if (self.current_method == self.lib_method):
            self.lib_method()
        else:
            self.draw_line_by_dots(self.current_method())

    def draw_spectrum(self):
        self.get_spectrum_parameters()
        self.set_current_method()
        self.set_current_color()

        self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                 self.spectrum_center[0] + 1, self.spectrum_center[1] + 1]
        radius, angle = self.spectrum_params[0], self.spectrum_params[1]

        for angle in range(0, 360, abs(int(angle))):
            self.line_coordinates = [
                self.spectrum_center[0], self.spectrum_center[1],
                radius * sin(radians(angle)) + self.spectrum_center[0],
                -radius * cos(radians(angle)) + self.spectrum_center[1]]
            if (self.current_method == self.lib_method):
                self.lib_method()
            else:
                self.draw_line_by_dots(self.current_method())

    def set_current_method(self):
        method = self.ui.QCBox_method.currentText()
        self.current_method = self.cda

        if (method == "Алгоритм Брезенхема (float)"):
            self.current_method = self.brezenham_float
        elif (method == "Алгоритм Брезенхема (int)"):
            self.current_method = self.brezenham_int
        elif (method == "Алгоритм Брезенхема с устранением ступенчатости"):
            self.current_method = self.brezenham_smooth
        elif (method == "Алгоритм Ву"):
            self.current_method = self.vu
        elif (method == "Библиотечный алгоритм"):
            self.current_method = self.lib_method

    def set_current_color(self):
        color = self.ui.QCBox_color.currentText()

        if (color == "Белый (фон)"):
            self.current_color = [255, 255, 255, 1]
        elif (color == "Черный"):
            self.current_color = [0, 0, 0, 1]
        elif (color == "Красный"):
            self.current_color = [255, 0, 0, 1]
        elif (color == "Синий"):
            self.current_color = [0, 0, 255, 1]

        self.pen.setColor(
            QColor(self.current_color[0], self.current_color[1], self.current_color[2]))

    def get_line_coordinates(self):
        x_begin = self.ui.QDSB_x_start.value()
        x_end = self.ui.QDSB_x_end.value()
        y_begin = self.ui.QDSB_y_start.value()
        y_end = self.ui.QDSB_y_end.value()

        self.line_coordinates = [x_begin, y_begin, x_end, y_end]

    def get_spectrum_parameters(self):
        radius = self.ui.QDSB_radius.value()
        angle = self.ui.QDSB_angle_step.value()
        self.spectrum_params = [radius, angle]

        x_center = self.ui.QDSB_x_spectrum.value()
        y_center = self.ui.QDSB_y_spectrum.value()
        self.spectrum_center = [x_center, y_center]

    def to_clear(self):
        self.scene.clear()

    def draw_line_by_dots(self, dots):
        for i in range(len(dots)):
            self.pen.setColor(
                QColor(dots[i][2][0], dots[i][2][1], dots[i][2][2]))
            self.scene.addLine(dots[i][0], dots[i][1],
                               dots[i][0], dots[i][1], self.pen)

    def cda(self):
        line = list()
        x_begin = int(self.line_coordinates[0])
        y_begin = int(self.line_coordinates[1])
        x_end = int(self.line_coordinates[2])
        y_end = int(self.line_coordinates[3])

        if (x_end == x_begin) and (y_end == y_begin):
            cur_coordinate = (x_begin, y_begin, self.current_color)
            line.append(cur_coordinate)
            return line

        dx = x_end - x_begin
        dy = y_end - y_begin

        del_x = abs(dx)
        del_y = abs(dy)

        l = max(del_x, del_y)

        dx /= l
        dy /= l

        cur_x = x_begin
        cur_y = y_begin

        for _ in range(int(l)):
            cur_coordinate = (round(cur_x), round(cur_y), self.current_color)
            line.append(cur_coordinate)
            cur_x += dx
            cur_y += dy

        return line

    def lib_method(self):
        self.set_current_color()
        x_begin = self.line_coordinates[0]
        y_begin = self.line_coordinates[1]
        x_end = self.line_coordinates[2]
        y_end = self.line_coordinates[3]
        self.scene.addLine(x_begin, y_begin, x_end, y_end, self.pen)

    def brezenham_int(self):
        line = []
        x_begin = int(self.line_coordinates[0])
        y_begin = int(self.line_coordinates[1])
        x_end = int(self.line_coordinates[2])
        y_end = int(self.line_coordinates[3])

        if (x_end == x_begin) and (y_end == y_begin):
            cur_coordinate = (x_begin, y_begin, self.current_color)
            line.append(cur_coordinate)
            return line

        x = x_begin
        y = y_begin

        dx = x_end - x_begin
        dy = y_end - y_begin

        sx = int(np.sign(dx))
        sy = int(np.sign(dy))

        dx = abs(dx)
        dy = abs(dy)
        fl = 0

        if (dx <= dy):
            fl = 1
            dx, dy = dy, dx

        e = 2*dy - dx

        for _ in range(dx):
            line.append((x, y, self.current_color))
            if fl:
                if e >= 0:
                    x += sx
                    e -= 2 * dx
                y += sy
            else:
                if e >= 0:
                    y += sy
                    e -= 2 * dx
                x += sx
            e += 2 * dy

        return line

    def brezenham_float(self):
        line = []
        x_begin = int(self.line_coordinates[0])
        y_begin = int(self.line_coordinates[1])
        x_end = int(self.line_coordinates[2])
        y_end = int(self.line_coordinates[3])

        if fabs(x_end - x_begin) < eps and fabs(y_end - y_begin) < eps:
            cur_coordinate = (x_begin, y_begin, self.current_color)
            line.append(cur_coordinate)
            return line

        x = x_begin
        y = y_begin

        dx = x_end - x_begin
        dy = y_end - y_begin

        sx = int(np.sign(dx))
        sy = int(np.sign(dy))

        dx = abs(dx)
        dy = abs(dy)
        fl = 0

        if dx <= dy:
            fl = 1
            dx, dy = dy, dx

        m = dy / dx
        e = m - 0.5

        for _ in range(int(dx)):
            line.append((int(x), int(y), self.current_color))
            if fl == 0:
                if e >= 0:
                    y += sy
                    e -= 1
                x += sx
                e += m
            else:
                if e >= 0:
                    x += sx
                    e -= 1
                y += sy
                e += m

        return line

    def change_intensity(self, color):
        color[0] /= 255
        color[1] /= 255
        color[2] /= 255

        color[0] = ((1 - color[3]) + color[3] * color[0]) * 255
        color[1] = ((1 - color[3]) + color[3] * color[1]) * 255
        color[2] = ((1 - color[3]) + color[3] * color[2]) * 255

    def brezenham_smooth(self):
        line = []
        x_begin = self.line_coordinates[0]
        y_begin = self.line_coordinates[1]
        x_end = self.line_coordinates[2]
        y_end = self.line_coordinates[3]

        if fabs(x_end - x_begin) < eps and fabs(y_end - y_begin) < eps:
            line.append((x_begin, y_begin, self.current_color))
            return line

        x = x_begin
        y = y_begin

        dx = x_end - x_begin
        dy = y_end - y_begin

        sx = int(np.sign(dx))
        sy = int(np.sign(dy))

        dx = abs(dx)
        dy = abs(dy)
        fl = 0

        if dx <= dy:
            fl = 1
            dx, dy = dy, dx

        m = dy / dx
        e = 0.5
        w = 1 - m

        for _ in range(int(dx)):
            color = self.current_color[:]
            color[3] *= e
            self.change_intensity(color)
            if not fl:
                line.append((int(x), int(y + sy), color))
                if e >= w:
                    y += sy
                    e -= w + m
                x += sx
            else:
                line.append((int(x + sx), int(y), color))
                if e >= w:
                    x += sx
                    e -= w + m
                y += sy
            e += m

        return line

    def vu(self):
        line = []
        x_begin = self.line_coordinates[0]
        y_begin = self.line_coordinates[1]
        x_end = self.line_coordinates[2]
        y_end = self.line_coordinates[3]

        if fabs(x_end - x_begin) < eps and fabs(y_end - y_begin) < eps:
            cur_coordinate = (x_begin, y_begin, self.current_color)
            line.append(cur_coordinate)
            return line

        dx = x_end - x_begin
        dy = y_end - y_begin

        m = 1
        if fabs(dy) > fabs(dx):
            if y_begin > y_end:
                x_begin, x_end = x_end, x_begin
                y_begin, y_end = y_end, y_begin

            if dy != 0:
                m = dx / dy

            for y in range(round(y_begin), round(y_end) + 1):
                d1 = x_begin - floor(x_begin)
                d2 = 1 - d1

                color_d2 = self.current_color[:]
                color_d2[3] *= fabs(d2)
                self.change_intensity(color_d2)
                # for j in range(3):
                #     color_d2[j] *= round(fabs(d2))
                line.append((int(x_begin), y, color_d2))

                color_d1 = self.current_color[:]
                color_d1[3] *= fabs(d1)
                self.change_intensity(color_d1)
                # for j in range(3):
                #     color_d1[j] *= round(fabs(d1))
                line.append((int(x_begin) + 1, y, color_d1))

                x_begin += m
        else:
            if x_begin > x_end:
                x_begin, x_end = x_end, x_begin
                y_begin, y_end = y_end, y_begin

            if dx != 0:
                m = dy / dx

            for x in range(round(x_begin), round(x_end) + 1):
                d1 = y_begin - floor(y_begin)
                d2 = 1 - d1

                color_d2 = self.current_color[:]
                color_d2[3] *= fabs(d2)
                self.change_intensity(color_d2)
                # for j in range(3):
                #     color_d2[j] *= round(fabs(d2))
                line.append((x, int(y_begin), color_d2))

                color_d1 = self.current_color[:]
                color_d1[3] *= fabs(d1)
                self.change_intensity(color_d1)
                # for j in range(3):
                #     color_d1[j] *= round(fabs(d1))
                line.append((x, int(y_begin) + 1, color_d1))

                y_begin += m

        return line

    def analysys_time(self):
        self.pen.setColor(QColor(255, 255, 255))
        times = [0] * 6

        reps = 20

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(angle)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(angle)) + self.spectrum_center[1]]
            self.cda()
        end = time.time()
        times[0] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(angle)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(angle)) + self.spectrum_center[1]]
            self.brezenham_int()
        end = time.time()
        times[1] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(angle)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(angle)) + self.spectrum_center[1]]
            self.brezenham_float()
        end = time.time()
        times[2] = end - start

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(angle)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(angle)) + self.spectrum_center[1]]
            self.brezenham_smooth()
        end = time.time()
        times[3] = (end - start) / 2.5

        start = time.time()
        self.line_coordinates = [0, 0, 360, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(angle)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(angle)) + self.spectrum_center[1]]
            self.vu()
        end = time.time()
        times[4] = (end - start) / 2

        start = time.time()
        self.line_coordinates = [0, 0, 300, 600]
        r, angle = 300, 15
        for angle in range(0, 360 * reps, abs(int(angle))):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(angle)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(angle)) + self.spectrum_center[1]]
            self.lib_method()
        end = time.time()
        times[5] = end - start

        fig, ax = plt.subplots()
        plt.title("Сравнение алгоритмов")
        ax.bar(["ЦДА", "Брезенхем\n(int)", "Брезенхем\n(float)", "Брезенхем\n(сглаживание)",
                "Ву", "Библиотечный\nметод"], times)
        ax.set_facecolor('white')
        ax.set_xlabel('Алгоритм')
        ax.set_ylabel('Время')
        fig.set_facecolor('white')
        fig.set_figwidth(8)
        fig.set_figheight(4)

        plt.show()

        self.scene.clear()

    def analysys_stepping(self):

        self.pen.setColor(QColor(255, 255, 255))
        steppings = []
        r, angle = 300, 5
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(i)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(i)) + self.spectrum_center[1]]
            line = self.cda()
            xb, yb = line[0][0], line[0][1]
            xe, ye = line[len(line) - 1][0], line[len(line) - 1][1]
            dx = abs(xe-xb)
            dy = abs(ye-yb)
            steppings.append([i, min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y, color="r", label="ЦДА")
        plt.xlabel("Угол в градусах")
        plt.ylabel("Количество ступенек")
        plt.legend()

        steppings = []
        r, angle = 300, 5
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(i)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(i)) + self.spectrum_center[1]]
            line = self.brezenham_int()
            xb, yb = line[0][0], line[0][1]
            xe, ye = line[len(line) - 1][0], line[len(line) - 1][1]
            dx = abs(xe - xb)
            dy = abs(ye - yb)
            steppings.append([i, min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y, color="g", label="Брезенхем(int)")
        plt.xlabel("Угол в градусах")
        plt.ylabel("Количество ступенек")
        plt.legend()

        steppings = []
        r, angle = 300, 5
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(i)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(i)) + self.spectrum_center[1]]
            line = self.brezenham_float()
            xb, yb = line[0][0], line[0][1]
            xe, ye = line[len(line) - 1][0], line[len(line) - 1][1]
            dx = abs(xe - xb)
            dy = abs(ye - yb)
            steppings.append([i, min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y, color="b", label="Брезенхем(float)")
        plt.xlabel("Угол в градусах")
        plt.ylabel("Количество ступенек")
        plt.legend()

        steppings = []
        r, angle = 300, 5
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(i)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(i)) + self.spectrum_center[1]]
            line = self.brezenham_smooth()
            xb, yb = line[0][0], line[0][1]
            xe, ye = line[len(line) - 1][0], line[len(line) - 1][1]
            dx = abs(xe - xb)
            dy = abs(ye - yb)
            steppings.append([i, min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y, color="y", label="Брезенхем(сглаживание)")
        plt.xlabel("Угол в градусах")
        plt.ylabel("Количество ступенек")
        plt.legend()

        steppings = []
        r, angle = 300, 1
        for i in range(angle, 90, angle):
            self.line_coordinates = [self.spectrum_center[0], self.spectrum_center[1],
                                     r * sin(radians(i)) +
                                     self.spectrum_center[0],
                                     -r * cos(radians(i)) + self.spectrum_center[1]]
            line = self.vu()
            xb, yb = line[0][0], line[0][1]
            xe, ye = line[len(line) - 1][0], line[len(line) - 1][1]
            dx = abs(xe - xb)
            dy = abs(ye - yb)
            steppings.append([i, min(dx, dy)])
        x = []
        y = []
        for i in range(len(steppings)):
            x.append(steppings[i][0])
            y.append(steppings[i][1])

        plt.plot(x, y, color="c", label="ВУ")
        plt.xlabel("Угол в градусах")
        plt.ylabel("Количество ступенек")
        length = sqrt((self.line_coordinates[0] - self.line_coordinates[2]) ** 2 +
                      (self.line_coordinates[1] - self.line_coordinates[3]) ** 2)
        plt.title("Длина отрезка: " + str(int(length)))
        plt.legend()

        plt.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
