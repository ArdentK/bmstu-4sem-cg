import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QGraphicsScene, QGraphicsView, QTableWidgetItem
from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtCore import Qt
import lab_01
from geom import get_solution, get_perpendicular_bisector
import math

dots = []


class App(QtWidgets.QMainWindow, lab_01.Ui_MainWindow):

    shift = 150

    def __init__(self):
        super(App, self).__init__()
        self.ui = lab_01.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_add_point.clicked.connect(self.add_point)
        self.ui.btn_del_all.clicked.connect(self.del_all_points)
        self.ui.btn_task.clicked.connect(self.output_task)
        self.ui.btn_edit_point.clicked.connect(self.edit_point)
        self.ui.btn_del_point.clicked.connect(self.del_point)
        self.ui.btn_run_app.clicked.connect(self.createGraphicView)
        self.ui.listWidget.currentItemChanged.connect(self.show_point)

        self.scene = QGraphicsScene()
        self.ui.QCanvas.setScene(self.scene)

    def show_point(self):
        value = self.ui.listWidget.currentItem()
        try:
            value = value.text().split(", ")
            value[0] = value[0][1:]
            value[1] = value[1][:-1]
            cur_item = str(value[0]) + ", " + str(value[1])
            self.ui.coordinate.setText(cur_item)

        except AttributeError:
            self.ui.coordinate.setText("")

    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.ui.QCanvas.setScene(self.scene)

        # width = self.ui.QCanvas.width()
        # height = self.ui.QCanvas.height()

        self.ui.QCanvas.setSceneRect(0, 0, 1, 1)
        self.ui.QCanvas.setAlignment(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.redBrush = QBrush(Qt.red)
        self.blackBrush = QBrush(Qt.black)

        self.redpen = QPen(Qt.red, 4)
        self.bluepen3 = QPen(Qt.blue, 3)
        self.greenpen2 = QPen(Qt.green, 2)
        self.blackpen = QPen(Qt.gray, 0.8)
        self.bluepen = QPen(Qt.blue, 3)
        self.graypen = QPen(Qt.gray, 3)

        self.run()

    def toCoord(self, x, y, _max_x, _min_x, _max_y, _min_y):
        width = self.ui.QCanvas.width()
        height = self.ui.QCanvas.height()

        # print(width, height)
        width -= self.shift
        height -= self.shift

        if (_max_x != _min_x):
            coef_x = width / (_max_x - _min_x)
        else:
            coef_x = -1
        if (_max_y != _min_y):
            coef_y = height / (_max_y - _min_y)
        else:
            coef_y = -1

        if (coef_x == -1):
            coef_x = coef_y + 1

        if (coef_y == -1):
            coef_y = coef_x + 1

        if (_max_x != _min_x):
            res_x = (x - _min_x) * min(coef_x, coef_y)
        else:
            res_x = width / 2

        if (_max_y != _min_y):
            res_y = (y - _min_y) * min(coef_x, coef_y)
        else:
            res_y = height / 2

        # print(x, y, res_x, res_y)
        # print()

        res_x += self.shift / 2
        res_y -= self.shift / 2

        res_y = height - res_y
        return res_x, res_y

    def run(self):
        global dots

        dots = []
        for index in range(self.ui.listWidget.count()):
            new_item = self.ui.listWidget.item(index).text().split(', ')
            new_item[0] = float(new_item[0][1:])
            new_item[1] = float(new_item[1][:-1])
            dots.append(new_item)

        if (len(dots) < 3):
            self.ui.text_answer.setText("")
            QMessageBox.critical(
                self, "Ошибка", "Недостаточное количество точек! (Их должно быть не меньше 3)")
            self.ui.coordinate.setText("")
            return

        solution = get_solution(dots)

        if (solution["difference"] == -1):
            self.ui.text_answer.setText("")
            QMessageBox.critical(
                self, "Ошибка", "Точки расположены на 1 прямой!")
            return

        ans = "Треугольник построен на точках с координатами: " + self.ui.listWidget.item(solution["ind_p1"]).text(
        ) + ", " + self.ui.listWidget.item(solution["ind_p2"]).text() + ", " + self.ui.listWidget.item(solution["ind_p3"]).text() + "\n"

        ans += "Координаты центра описанной окружности: " + \
            "(" + str("{:.4}".format(solution["center"][0])) + ", " + str(
                "{:.4}".format(solution["center"][1])) + ")\n"

        ans += "Радиус описанной окружности: " + \
            str("{:.4}".format(solution["radius"])) + "\n"

        ans += "Площадь круга: " + \
            str("{:.4}".format(solution["circle_area"])) + "\n"
        ans += "Площадь треугольника: " + \
            str("{:.4}".format(solution["triangle_area"])) + "\n"

        ans += "Разница между полощадями окружности и треугольника: " + \
            str("{:.4}".format(solution["difference"])) + "\n"

        self.ui.text_answer.setText(ans)

        p1 = solution["ind_p1"]
        p2 = solution["ind_p2"]
        p3 = solution["ind_p3"]
        center = solution["center"]
        radius = solution["radius"]

        begin1, end1, begin2, end2 = get_perpendicular_bisector(
            dots[p1], dots[p2], dots[p3], radius, radius)

        max_x2 = max(dots[p1][0], dots[p2][0], dots[p3][0], begin1[0], end1[0],
                     begin2[0], end2[0], center[0] - radius, center[0] + radius)
        min_x2 = min(dots[p1][0], dots[p2][0], dots[p3][0], begin1[0], end1[0],
                     begin2[0], end2[0], center[0] - radius, center[0] + radius)
        max_y2 = max(dots[p1][1], dots[p2][1], dots[p3][1], begin1[1], end1[1],
                     begin2[1], end2[1], center[1] - radius, center[1] + radius)
        min_y2 = min(dots[p1][1], dots[p2][1], dots[p3][1], begin1[1], end1[1],
                     begin2[1], end2[1], center[1] - radius, center[1] + radius)

        self.scene.clear()

        graph_cenx, graph_ceny = self.toCoord(
            center[0], center[1], max_x2, min_x2, max_y2, min_y2)
        self.scene.addEllipse(graph_cenx - 1.5, graph_ceny - 1.5,
                              3, 3, self.blackpen, self.blackBrush)

        graph_xp1, graph_yp1 = self.toCoord(
            dots[p1][0], dots[p1][1], max_x2, min_x2, max_y2, min_y2)

        graph_xp2, graph_yp2 = self.toCoord(
            dots[p2][0], dots[p2][1], max_x2, min_x2, max_y2, min_y2)

        graph_xp3, graph_yp3 = self.toCoord(
            dots[p3][0], dots[p3][1], max_x2, min_x2, max_y2, min_y2)

        graph_xb1, graph_yb1 = self.toCoord(
            begin1[0], begin1[1], max_x2, min_x2, max_y2, min_y2)
        # graph_xe1, graph_ye1 = self.toCoord(end1[0], end1[1], max_x2, min_x2, max_y2, min_y2)

        graph_xb2, graph_yb2 = self.toCoord(
            begin2[0], begin2[1], max_x2, min_x2, max_y2, min_y2)
        graph_xe2, graph_ye2 = self.toCoord(
            end2[0], end2[1], max_x2, min_x2, max_y2, min_y2)

        self.scene.addLine(graph_xb1, graph_yb1, graph_cenx,
                           graph_ceny, self.blackpen)
        self.scene.addLine(graph_xb2, graph_yb2, graph_cenx,
                           graph_ceny, self.blackpen)

        self.scene.addLine(graph_xp1, graph_yp1, graph_xp2,
                           graph_yp2, self.bluepen3)
        self.scene.addLine(graph_xp1, graph_yp1, graph_xp3,
                           graph_yp3, self.bluepen3)
        self.scene.addLine(graph_xp2, graph_yp2, graph_xp3,
                           graph_yp3, self.bluepen3)

        # h = sqrt(2) * radius
        graph_x, graph_y = self.toCoord(
            center[0] - radius, center[1] - radius, max_x2, min_x2, max_y2, min_y2)
        graph_x2, graph_y2 = self.toCoord(
            center[0] + radius, center[1] + radius, max_x2, min_x2, max_y2, min_y2)

        self.scene.addEllipse(graph_x, graph_y, graph_x2 -
                              graph_x, graph_y2 - graph_y, self.greenpen2)

        self.scene.addEllipse(graph_xp1 - 1.5, graph_yp1 - 1.5,
                              3, 3, self.redpen, self.redBrush)
        self.scene.addEllipse(graph_xp2 - 1.5, graph_yp2 - 1.5,
                              3, 3, self.redpen, self.redBrush)
        self.scene.addEllipse(graph_xp3 - 1.5, graph_yp3 - 1.5,
                              3, 3, self.redpen, self.redBrush)

        dot_label = self.scene.addText("{:g}".format(
            p1 + 1) + " ( " + "{:.4}".format(dots[p1][0]) + ", " + "{:.4}".format(dots[p1][1]) + " )")
        dot_label.setPos(graph_xp1 - 35, graph_yp1 - 35)

        dot_label = self.scene.addText("{:g}".format(
            p2 + 1) + " ( " + "{:.4}".format(dots[p2][0]) + ", " + "{:.4}".format(dots[p2][1]) + " )")
        dot_label.setPos(graph_xp2 - 35, graph_yp2 - 35)

        dot_label = self.scene.addText("{:g}".format(
            p3 + 1) + " ( " + "{:.4}".format(dots[p3][0]) + ", " + "{:.4}".format(dots[p3][1]) + " )")
        dot_label.setPos(graph_xp3 - 35, graph_yp3 - 35)

        dot_label = self.scene.addText(
            "( " + "{:.4}".format(center[0]) + "; " + "{:.4}".format(center[1]) + " )")
        dot_label.setPos(graph_cenx - 35, graph_ceny - 35)

    def output_task(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(
            "На плоскости дано множество точек. Найти такой треугольник с вершинами в этих точках, у которого разность площадей описанной окружности и треугольника максимальны.")
        msgBox.setWindowTitle("Задание")
        msgBox.exec()

    def del_all_points(self):
        self.ui.listWidget.clear()
        self.ui.text_answer.clear()
        self.scene.clear()
        # dots.clear()

    def add_point(self):
        global dots

        textboxValue = self.ui.coordinate.text()
        coordinates = textboxValue.split(",")

        if (len(coordinates) != 2):
            QMessageBox.critical(
                self, "Ошибка", "Неверное количество координат!")
            self.ui.coordinate.setText("")
            return

        for i in range(2):
            try:
                coordinates[i] = float(coordinates[i])
            except ValueError:
                QMessageBox.critical(
                    self, "Ошибка", "Координаты должны быть числами!")
                self.ui.coordinate.setText("")

                return

        self.ui.listWidget.addItem(
            "(" + str(coordinates[0]) + ", " + str(coordinates[1]) + ")")
        self.ui.coordinate.setText("")

        self.scene.clear()
        # dots.append(coordinates)

    def edit_point(self):
        sel_dots = self.ui.listWidget.selectedItems()
        for item in sel_dots:
            new_coordinates = self.ui.coordinate.text().split(',')
            if (len(new_coordinates) != 2):
                QMessageBox.critical(
                    self, "Ошибка", "Неверное количество координат!")
                self.ui.coordinate.setText("")
                return

            for i in range(2):
                try:
                    new_coordinates[i] = float(new_coordinates[i])
                except ValueError:
                    QMessageBox.critical(
                        self, "Ошибка", "Координаты должны быть числами!")
                    self.ui.coordinate.setText("")
                    return
            item.setText(
                "(" + str(new_coordinates[0]) + ", " + str(new_coordinates[1]) + ")")
            self.ui.coordinate.setText("")

    def del_point(self):
        row = self.ui.listWidget.currentRow()
        if (row == -1):
            QMessageBox.critical(
                self, "Ошибка", "Выделите точку, которую следует удалить!")
            return
        self.ui.listWidget.takeItem(row)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
