import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QGraphicsScene, QGraphicsView, QTableWidgetItem, QStyleFactory
from PyQt5.QtGui import QBrush, QPen, QPainter, QColor
from PyQt5.QtCore import Qt
import mainwindow
from math import *
import numpy as np
import time
import matplotlib.pyplot as plt
import copy as copy

eps = 1e-5


class App(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self):
        super(App, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.QCB_color.activated.connect(self.set_current_color)

        self.ui.QPBtn_center.clicked.connect(self.set_center)
        self.ui.QPBtn_clear.clicked.connect(self.to_clear)
        self.ui.QPBtn_draw_circle.clicked.connect(self.draw_circle)
        self.ui.QPBtn_draw_ellipse.clicked.connect(self.draw_ellipse)
        self.ui.QPBtn_draw_concentric_circles.clicked.connect(
            self.draw_circles_with_ui_configuration)
        self.ui.QPBtn_draw_concentric_ellipses.clicked.connect(
            self.draw_ellipses_with_ui_configuration)
        self.ui.QPBtn_analytics.clicked.connect(self.time_analytics)

        self.createGraphicView()

    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()

        self.ui.graphicsView.setSceneRect(0, 0, width-10, height-10)
        self.ui.graphicsView.setAlignment(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.pen = QPen(Qt.red, 1)

        self.color = [255, 0, 0]

        self.set_current_color()
        self.set_circle_method()
        self.get_center()

    def get_center(self):
        self.center = [self.ui.QSB_x_center.value(),
                       self.ui.QSB_y_center.value()]

    def set_center(self):
        width = self.ui.graphicsView.width()
        height = self.ui.graphicsView.height()

        self.ui.QSB_x_center.setValue(width/2)
        self.ui.QSB_y_center.setValue(height/2)

    def set_current_color(self):
        color = self.ui.QCB_color.currentText()

        if (color == "Белый (фон)"):
            self.color = [255, 255, 255]
        elif (color == "Черный"):
            self.color = [0, 0, 0]
        elif (color == "Красный"):
            self.color = [255, 0, 0]
        elif (color == "Синий"):
            self.color = [0, 0, 255]

        self.pen.setColor(
            QColor(self.color[0], self.color[1], self.color[2]))

    def set_circle_method(self):
        method = self.ui.QCB_algorithm.currentText()
        self.method = self.canonical_circle

        if (method == "Параметрическое уравнение"):
            self.method = self.parametric_circle
        elif (method == "Алгоритм Брезенхема"):
            self.method = self.brezenham_circle
        elif (method == "Алгоритм средней точки"):
            self.method = self.midpoint_circle
        elif (method == "Библиотечный алгоритм"):
            self.method = self.library_method_circle

    def set_ellipse_method(self):
        method = self.ui.QCB_algorithm.currentText()
        self.method = self.canonical_ellipse

        if (method == "Параметрическое уравнение"):
            self.method = self.parametric_ellipse
        elif (method == "Алгоритм Брезенхема"):
            self.method = self.brezenham_ellipse
        elif (method == "Алгоритм средней точки"):
            self.method = self.midpoint_ellipse
        elif (method == "Библиотечный алгоритм"):
            self.method = self.library_method_ellipse

    def canonical_circle(self):
        octant = list()
        dot = [self.center[0], self.center[1]]

        while (dot[0] < self.center[0] + round((self.radius)/sqrt(2)) + 1):
            dot[1] = self.center[1] + \
                round(sqrt(self.radius**2 - (dot[0] - self.center[0])**2))
            octant.append(dot.copy())
            dot[0] += 1

        return octant

    def parametric_circle(self):
        octant = []
        dot = [0, 0]

        t = 0
        # расстояние между рисуемыми пикселями пропорционально углу между ними
        # (вершина угла находится в центре окружности)
        step = 1 / self.radius

        while (t < pi / 4 + step):
            dot[0] = round(self.center[0] + cos(t) * self.radius)
            dot[1] = round(self.center[1] + sin(t) * self.radius)
            octant.append(dot.copy())
            t += step

        return octant

    def midpoint_circle(self):
        # вводим функцию, которая содержит разность квадрата расстояния от центра
        # окружности до «средней точки» рассматриваемого на текущий момент пикселя
        # и квадрата расстояния до идеальной окружности
        octant = []
        dot = [0, self.radius]
        d = 1 - self.radius

        moved_dot = [dot[0] + self.center[0], dot[1] + self.center[1]]
        octant.append(moved_dot)

        while (dot[1] > dot[0]):
            if (d < 0):
                d += 2 * dot[0] + 3
            else:
                d += 2 * (dot[0] - dot[1]) + 5
                dot[1] -= 1
            dot[0] += 1
            moved_dot = [dot[0] + self.center[0], dot[1] + self.center[1]]
            octant.append(moved_dot)

        return octant

    def brezenham_circle(self):
        # окружность строится путем рассмотрения возможных ситуаций прохода прямой
        # и, исходя из этого положения, рассмотрения расстояния до ближайших пикселей
        octant = []
        dot = [0, self.radius]
        d = 2 * (1 - self.radius)

        moved_dot = [dot[0] + self.center[0], dot[1] + self.center[1]]
        octant.append(moved_dot)

        while (dot[1] > dot[0]):
            if (d <= 0):
                d1 = 2 * (d + dot[1]) - 1
                dot[0] += 1
                if (d1 <= 0):
                    # горизонтальный шаг
                    d += 2 * dot[0] + 1
                else:
                    # диагональный шаг
                    dot[1] -= 1
                    d += 2 * (dot[0] - dot[1] + 1)
            else:
                d2 = 2 * (d - dot[0]) - 1
                dot[1] -= 1
                if (d2 <= 0):
                    # диагональный шаг
                    dot[0] += 1
                    d += 2 * (dot[0] - dot[1] + 1)
                else:
                    # вертикальный шаг
                    d -= 2 * dot[1] + 1
            moved_dot = [dot[0] + self.center[0], dot[1] + self.center[1]]
            octant.append(moved_dot)

        return octant

    def library_method_circle(self):
        # self.set_current_color()
        self.scene.addEllipse(
            self.center[0] - self.radius, self.center[1] - self.radius, self.radius*2, self.radius*2, self.pen)

    def draw_circle(self):
        self.set_circle_method()
        self.set_current_color()
        self.get_center()
        self.radius = self.ui.QSB_radius.value()
        if (self.method == self.library_method_circle):
            self.library_method_circle()
        else:
            self.draw_octant_by_dots(self.method())

    def canonical_ellipse(self):
        quarter = []
        dot = [self.center[0], self.center[1]]
        limit = self.center[0] + round((self.semiaxis_a ** 2 /
                                        sqrt(self.semiaxis_a**2 + self.semiaxis_b**2)))
        while (dot[0] <= limit):
            dot[1] = self.center[1] + round(sqrt(self.semiaxis_a**2 - (
                dot[0] - self.center[0])**2) * self.semiaxis_b / self.semiaxis_a)
            quarter.append(dot.copy())
            dot[0] += 1

        dot[1] = self.center[1]
        limit = self.center[1] + round((self.semiaxis_b **
                                        2 / sqrt(self.semiaxis_a**2 + self.semiaxis_b**2)))

        while (dot[1] <= limit):
            dot[0] = self.center[0] + round(sqrt(self.semiaxis_b**2 - (
                dot[1] - self.center[1])**2) * self.semiaxis_a / self.semiaxis_b)
            quarter.append(dot.copy())
            dot[1] += 1

        return quarter

    def parametric_ellipse(self):
        quarter = []
        dot = [self.center[0], self.center[1]]
        limit = self.center[1] + round((self.semiaxis_b **
                                        2 / sqrt(self.semiaxis_a**2 + self.semiaxis_b**2)))
        t = 0
        step = 1 / self.semiaxis_b

        while (dot[1] < limit):
            dot[0] = self.center[0] + round(cos(t) * self.semiaxis_a)
            dot[1] = self.center[1] + round(sin(t) * self.semiaxis_b)
            quarter.append(dot.copy())
            t += step

        dot[1] = self.center[1]
        step = 1 / self.semiaxis_a

        while (dot[0] > self.center[0]):
            dot[0] = self.center[0] + round(cos(t) * self.semiaxis_a)
            dot[1] = self.center[1] + round(sin(t) * self.semiaxis_b)
            quarter.append(dot.copy())
            t += step

        return quarter

    def midpoint_ellipse(self):
        quarter = []
        dot = [0, self.semiaxis_b]

        sqr_a = self.semiaxis_a**2
        sqr_b = self.semiaxis_b**2

        sqr_a_2 = sqr_a * 2
        sqr_b_2 = sqr_b * 2

        f = sqr_b - sqr_a * self.semiaxis_b + 0.25 * sqr_a

        dx = sqr_b_2 * dot[0]
        dy = sqr_a_2 * dot[1]

        while (dx < dy):
            moved_dot = [dot[0] + self.center[0], dot[1] + self.center[1]]
            quarter.append(moved_dot)

            dot[0] += 1
            dx += sqr_b_2

            if (f >= 0):
                dot[1] -= 1
                dy -= sqr_a_2
                f -= dy

            f += dx + sqr_b

        f += 3 * (sqr_a - sqr_b) / 4 - \
            (sqr_b_2 * dot[0] + sqr_a_2 * dot[1]) / 2

        while (dot[1] >= 0):
            moved_dot = [dot[0] + self.center[0], dot[1] + self.center[1]]
            quarter.append(moved_dot)

            dot[1] -= 1
            dy -= sqr_a_2

            if (f <= 0):
                dot[0] += 1
                dx += sqr_b_2
                f += dx

            f -= dy - sqr_a

        return quarter

    def brezenham_ellipse(self):
        quarter = []
        dot = [0, self.semiaxis_b]

        d = self.semiaxis_a**2 + self.semiaxis_b**2 - \
            2 * self.semiaxis_a**2 * self.semiaxis_b

        moved_dot = [dot[0] + self.center[0], dot[1] + self.center[1]]
        quarter.append(moved_dot)

        sqr_a = self.semiaxis_a**2
        sqr_b = self.semiaxis_b**2

        sqr_a_2 = sqr_a * 2
        sqr_b_2 = sqr_b * 2

        while (dot[1] > 0):
            if (d <= 0):
                d1 = 2 * d + sqr_a_2 * dot[1] - sqr_a
                dot[0] += 1
                if (d1 <= 0):
                    # Горизонтальный шаг
                    d += (2 * dot[0] + 1) * sqr_b
                else:
                    # Диагональный шаг
                    dot[1] -= 1
                    d += sqr_b * (2 * dot[0] + 1) + sqr_a * (1 - 2 * dot[1])
            else:
                d2 = 2 * d - sqr_b_2 * dot[0] - sqr_b
                dot[1] -= 1
                if (d2 <= 0):
                    # Диагональный шаг
                    dot[0] += 1
                    d += sqr_b * (2 * dot[0] + 1) + sqr_a * (1 - 2 * dot[1])
                else:
                    # Вертикальный шаг
                    d += (1 - 2 * dot[1]) * sqr_a
            moved_dot = [dot[0] + self.center[0], dot[1] + self.center[1]]
            quarter.append(moved_dot)

        return quarter

    def library_method_ellipse(self):
        self.scene.addEllipse(
            self.center[0] - self.semiaxis_a, self.center[1] - self.semiaxis_b, 2 * self.semiaxis_a, 2 * self.semiaxis_b, self.pen)

    def draw_ellipse(self, dots):
        self.set_ellipse_method()
        self.set_current_color()
        self.get_center()
        self.semiaxis_a = self.ui.QSB_semiaxis_a.value()
        self.semiaxis_b = self.ui.QSB_semiaxis_b.value()
        self.get_center()
        if (self.method == self.library_method_ellipse):
            self.library_method_ellipse()
        else:
            self.draw_quarter_by_dots(self.method())

    def draw_quarter_by_dots(self, dots):
        for i in range(len(dots)):
            self.scene.addLine(dots[i][0], dots[i][1],
                               dots[i][0], dots[i][1], self.pen)

            self.scene.addLine(2 * self.center[0] - dots[i][0], dots[i][1],
                               2 * self.center[0] - dots[i][0], dots[i][1], self.pen)

            self.scene.addLine(2 * self.center[0] - dots[i][0], 2 * self.center[1] - dots[i][1],
                               2 * self.center[0] - dots[i][0], 2 * self.center[1] - dots[i][1], self.pen)

            self.scene.addLine(dots[i][0], 2 * self.center[1] - dots[i][1],
                               dots[i][0], 2 * self.center[1] - dots[i][1], self.pen)

    def draw_octant_by_dots(self, dots):
        for i in range(len(dots)):
            self.scene.addLine(dots[i][0], dots[i][1],
                               dots[i][0], dots[i][1], self.pen)
            self.scene.addLine(2 * self.center[0] - dots[i][0], dots[i][1],
                               2 * self.center[0] - dots[i][0], dots[i][1], self.pen)
            self.scene.addLine(2 * self.center[0] - dots[i][0], 2 * self.center[1] - dots[i][1],
                               2 * self.center[0] - dots[i][0], 2 * self.center[1] - dots[i][1], self.pen)
            self.scene.addLine(dots[i][0], 2 * self.center[1] - dots[i][1],
                               dots[i][0], 2 * self.center[1] - dots[i][1], self.pen)

            self.scene.addLine(-dots[i][1] + sum(self.center), dots[i][0] + self.center[1] - self.center[0],
                               -dots[i][1] + sum(self.center), dots[i][0] + self.center[1] - self.center[0], self.pen)
            self.scene.addLine(dots[i][1] + self.center[0] - self.center[1], -dots[i][0] + sum(self.center),
                               dots[i][1] + self.center[0] - self.center[1], -dots[i][0] + sum(self.center), self.pen)
            self.scene.addLine(-dots[i][1] + sum(self.center), -dots[i][0] + sum(self.center),
                               -dots[i][1] + sum(self.center), -dots[i][0] + sum(self.center), self.pen)
            self.scene.addLine(dots[i][0], 2 * self.center[1] - dots[i][1],
                               dots[i][0], 2 * self.center[1] - dots[i][1], self.pen)
            self.scene.addLine(dots[i][1] + self.center[0] - self.center[1], dots[i][0] + self.center[1] - self.center[0],
                               dots[i][1] + self.center[0] - self.center[1], dots[i][0] + self.center[1] - self.center[0], self.pen)

    def draw_concentric_circles(self):
        if (self.circles_amount != 0):
            self.end_radius = self.start_radius + self.step * self.circles_amount

        for r in range(self.start_radius, self.end_radius + 1, self.step):
            self.radius = r
            if (self.method == self.library_method_circle):
                self.library_method_circle()
            else:
                self.draw_octant_by_dots(self.method())

    def draw_circles_with_ui_configuration(self):
        self.set_current_color()
        self.set_circle_method()
        self.get_center()
        self.get_concentric_circles_parameters()

        self.draw_concentric_circles()

    def draw_ellipses_with_ui_configuration(self):
        self.set_current_color()
        self.set_ellipse_method()
        self.get_center()
        self.get_concentric_ellipses_parameters()

        self.draw_concentric_ellipses()

    def draw_concentric_ellipses(self):
        self.semiaxis_a = self.start_semiaxis[0]
        self.semiaxis_b = self.start_semiaxis[1]

        for _ in range(self.ellipses_amount):
            if (self.method == self.library_method_ellipse):
                self.library_method_ellipse()
            else:
                self.draw_quarter_by_dots(self.method())
            self.semiaxis_a += self.step_semiaxis[0]
            self.semiaxis_b += self.step_semiaxis[1]

    def get_concentric_ellipses_parameters(self):
        self.start_semiaxis = [
            self.ui.QSB_start_semiaxis_a.value(), self.ui.QSB_start_semiaxis_b.value()]
        self.step_semiaxis = [
            self.ui.QSB_step_semiaxis_a.value(), self.ui.QSB_step_semiaxis_b.value()]
        self.ellipses_amount = self.ui.QSB_ellipses_count.value()

        if ((self.step_semiaxis[0] - self.start_semiaxis[0] == 0) and (self.step_semiaxis[1] - self.start_semiaxis[1] == 0)):
            QMessageBox.critical(
                self, "Предупреждение", "Количество эллипсов и разница между начальными и конечными значениями полуосей равны нулю. \nВы уверены в правильности введенных данных?")

    def get_concentric_circles_parameters(self):
        self.start_radius = self.ui.QSB_start_radius.value()
        self.end_radius = self.ui.QSB_end_radius.value()
        self.circles_amount = self.ui.QSB_circles_count.value()
        self.step = self.ui.QSB_step_radius.value()

        if ((self.end_radius - self.start_radius == 0) and self.circles_amount == 0):
            QMessageBox.critical(
                self, "Предупреждение", "Количество окружностей и разница между начальными и конечным радиусами равна 0.\nВы уверены в правильности введенных данных?")

    def time_analytics(self):
        self.pen.setColor(Qt.white)

        r = np.arange(1, 100, 5)
        semiaxis_a = np.arange(2, 100, 2)
        semiaxis_b = np.arange(1, 50, 1)
        reps = 100

        canonical_times = []
        for i in range(len(r)):
            self.radius = r[i]
            self.get_center()
            start = time.time()
            for _ in range(reps):
                self.canonical_circle()
            end = time.time()
            canonical_times.append((end - start) / reps)

        parametric_times = []
        for i in range(len(r)):
            self.radius = r[i]
            self.get_center()
            start = time.time()
            for _ in range(reps):
                self.parametric_circle()
            end = time.time()
            parametric_times.append((end - start) / reps)

        midpoint_times = []
        for i in range(len(r)):
            self.radius = r[i]
            self.get_center()
            start = time.time()
            for _ in range(reps):
                self.midpoint_circle()
            end = time.time()
            midpoint_times.append((end - start) / reps)

        brezenham_times = []
        for i in range(len(r)):
            self.radius = r[i]
            self.get_center()
            start = time.time()
            for _ in range(reps):
                self.brezenham_circle()
            end = time.time()
            brezenham_times.append((end - start) / reps)

        lib_times = []
        for i in range(len(r)):
            self.radius = r[i]
            self.get_center()
            start = time.time()
            for _ in range(reps):
                self.library_method_circle()
            end = time.time()
            lib_times.append((end - start) / reps)

        canonical_ellipse_times = []
        for i in range(len(semiaxis_a)):
            self.semiaxis_a = semiaxis_a[i]
            self.semiaxis_b = semiaxis_b[i]
            self.get_center()
            start = time.time()
            for _ in range(reps):
                self.canonical_ellipse()
            end = time.time()
            canonical_ellipse_times.append((end - start) / reps)

        parametric_ellipse_times = []
        for i in range(len(semiaxis_a)):
            self.semiaxis_a = semiaxis_a[i]
            self.semiaxis_b = semiaxis_b[i]
            self.get_center()
            start = time.time()
            for _ in range(reps):
                self.parametric_ellipse()
            end = time.time()
            parametric_ellipse_times.append((end - start) / reps)

        midpoint_ellipse_times = []
        for i in range(len(semiaxis_a)):
            self.semiaxis_a = semiaxis_a[i]
            self.semiaxis_b = semiaxis_b[i]
            self.get_center()
            start = time.time()
            for _ in range(reps):
                self.midpoint_ellipse()
            end = time.time()
            midpoint_ellipse_times.append((end - start) / reps)

        brezenham_ellipse_times = []
        for i in range(len(semiaxis_a)):
            self.semiaxis_a = semiaxis_a[i]
            self.semiaxis_b = semiaxis_b[i]
            self.get_center()
            start = time.time()
            for _ in range(reps):
                self.brezenham_ellipse()
            end = time.time()
            brezenham_ellipse_times.append((end - start) / reps)

        lib_ellipse_times = []
        for i in range(len(semiaxis_a)):
            self.semiaxis_a = semiaxis_a[i]
            self.semiaxis_b = semiaxis_b[i]
            self.get_center()
            start = time.time()
            for _ in range(reps):
                self.library_method_ellipse()
            end = time.time()
            lib_ellipse_times.append((end - start) / reps)

        fig, ax = plt.subplots(2, 1, constrained_layout=True)

        ax[0].set_title("Построение окружностей")
        ax[0].plot(r, canonical_times, label="Каноническое уравнение")
        ax[0].plot(r, parametric_times, label="Параметрическое уравнение")
        ax[0].plot(r, midpoint_times, label="Алгоритм средней точки")
        ax[0].plot(r, brezenham_times, label="Алгоритм Брезенхема")
        ax[0].plot(r, lib_times, label="АБиблиотечный алгоритм")
        ax[0].set_facecolor('white')
        ax[0].set_xlabel('Радиус')
        ax[0].set_ylabel('Время')
        ax[0].legend()

        ax[1].set_title("Построение эллипсов. (a : b = 2 : 1)")
        ax[1].plot(semiaxis_a, canonical_ellipse_times,
                   label="Каноническое уравнение")
        ax[1].plot(semiaxis_a, parametric_ellipse_times,
                   label="Параметрическое уравнение")
        ax[1].plot(semiaxis_a, midpoint_ellipse_times,
                   label="Алгоритм средней точки")
        ax[1].plot(semiaxis_a, brezenham_ellipse_times,
                   label="Алгоритм Брезенхема")
        ax[1].plot(semiaxis_a, lib_ellipse_times,
                   label="Библиотечный алгоритм")
        ax[1].set_facecolor('white')
        ax[1].set_xlabel('Полуось a')
        ax[1].set_ylabel('Время')
        ax[1].legend()

        fig.set_facecolor('white')
        # fig.set_figwidth(16)
        # fig.set_figheight(8)

        plt.show()

        self.to_clear()

    def to_clear(self):
        self.scene.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
