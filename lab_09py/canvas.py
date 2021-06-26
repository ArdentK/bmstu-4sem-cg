from copy import deepcopy

from structures import Dot
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtGui import QColor, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMessageBox


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.polygon_color = Qt.blue
        self.cutter_color = Qt.red
        self.result_color = Qt.black

        self.cutter = []
        self.polygon = []

        self.last_cutter_point = None
        self.last_polygon_point = None

        self.flag_locked_cutter = False
        self.flag_locked_polygon = False

    def image_init(self):
        self.image = QImage(self.width(), self.height(),
                            QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)

    def set_ui(self, ui):
        self.ui = ui

    def image_set(self):
        self.pixmap = QPixmap().fromImage(self.image)
        self.setPixmap(self.pixmap)

    def clear(self):
        self.image_init()
        self.image_set()
        self.polygon.clear()
        self.cutter.clear()
        self.flag_locked_cutter = None
        self.flag_locked_polygon = None
        self.last_point = None

    def mousePressEvent(self, event):
        position = Dot(event.pos().x(), event.pos().y())
        if self.ui.QRB_cutter.isChecked():
            if event.buttons() == Qt.LeftButton:
                exactly = QApplication.keyboardModifiers() & Qt.ControlModifier
                self.add_cutter_dot(position, exactly)
            elif event.buttons() == Qt.RightButton:
                self.close_cutter()
        elif self.ui.QRB_polygon.isChecked():
            if event.buttons() == Qt.LeftButton:
                exactly = QApplication.keyboardModifiers() & Qt.ControlModifier
                self.add_polygon_dot(position, exactly=exactly)
            elif event.buttons() == Qt.RightButton:
                self.close_poly()

    def add_polygon_dot(self, pos: Dot, exactly=False):
        if exactly:
            last_vertex = self.polygon[-1]
            dx, dy = abs(pos.x - last_vertex.x), abs(pos.y - last_vertex.y)
            if dx < dy:
                pos.x = last_vertex.x
            else:
                pos.y = last_vertex.y

        self.polygon.append(pos)

        qp = QPainter(self.image)
        qp.setPen(QPen(self.polygon_color, 1))
        if len(self.polygon) > 1:
            qp.drawLine(self.polygon[-2].to_qpoint(),
                        self.polygon[-1].to_qpoint())
        qp.end()

        self.image_set()

    def add_cutter_dot(self, pos: Dot, exactly=False):
        if exactly:
            last_vertex = self.cutter[-1]
            dx, dy = abs(pos.x - last_vertex.x), abs(pos.y - last_vertex.y)
            if dx < dy:
                pos.x = last_vertex.x
            else:
                pos.y = last_vertex.y

        self.cutter.append(pos)

        qp = QPainter(self.image)
        qp.setPen(QPen(self.cutter_color, 1))
        if len(self.cutter) > 1:
            qp.drawLine(self.cutter[-2].to_qpoint(),
                        self.cutter[-1].to_qpoint())
        qp.end()

        self.image_set()

    def close_cutter(self):
        if len(self.cutter) < 3:
            return

        qp = QPainter(self.image)
        qp.setPen(QPen(self.cutter_color, 1))
        self.flag_locked_cutter = True
        qp.drawLine(self.cutter[-1].to_qpoint(),
                    self.cutter[0].to_qpoint())
        qp.end()

        self.image_set()

    def close_poly(self):
        if len(self.polygon) < 3:
            return

        qp = QPainter(self.image)
        qp.setPen(QPen(self.polygon_color, 1))
        self.flag_locked_polygon = True
        qp.drawLine(self.polygon[-1].to_qpoint(), self.polygon[0].to_qpoint())
        qp.end()

        self.image_set()

    # Отрисовка части отрезка
    def draw_polygon(self, polygon, colour_result):
        qp = QPainter(self.image)
        qp.setPen(QPen(colour_result, 2))
        qp.drawLine(polygon[-1].to_qpoint(), polygon[0].to_qpoint())
        for i in range(len(polygon) - 1):
            qp.drawLine(polygon[i].to_qpoint(), polygon[i + 1].to_qpoint())
        qp.end()

        self.image_set()

    def cut_polygon(self):
        if self.polygon == []:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не был введен многоугольник")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return

        if self.cutter == []:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не был введен отсекатель")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return

        if self.is_cutter_convex() == False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Отсекатель не является выпуклым")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return

        result_polygon = self.cut_off_sutherland_hodgman(
            self.cutter, self.polygon)
        if result_polygon:
            self.draw_polygon(result_polygon, self.result_color)

    def get_vector_coordinates(self, point_1: Dot, point_2: Dot):
        return [point_1.x - point_2.x, point_1.y - point_2.y]

    # Вычислить векторное произведение и вернуть его знак
    def compulate_sign_mul_vectors(self, vector_1, vector_2):
        angle = vector_1[0] * vector_2[1] - vector_1[1] * vector_2[0]
        return angle

    # Проверка, является ли отсекатель выпуклым
    def is_cutter_convex(self):
        flag = True
        vector_1 = self.get_vector_coordinates(self.cutter[-1], self.cutter[0])
        vector_2 = self.get_vector_coordinates(self.cutter[0], self.cutter[1])
        sign_mul_vectors = self.compulate_sign_mul_vectors(vector_1, vector_2)

        if self.flag_locked_cutter == True:
            for i in range(len(self.cutter) - 2):
                vector_1 = self.get_vector_coordinates(
                    self.cutter[i], self.cutter[i + 1])
                vector_2 = self.get_vector_coordinates(
                    self.cutter[i + 1], self.cutter[i + 2])
                curr_sign_mul_vectors = self.compulate_sign_mul_vectors(
                    vector_1, vector_2)
                # если вект. произв. имеют разный знак или одно из них ноль
                if curr_sign_mul_vectors * sign_mul_vectors <= 0:
                    flag = False
                    break

        if flag == True:
            vector_1 = self.get_vector_coordinates(
                self.cutter[-2], self.cutter[-1])
            vector_2 = self.get_vector_coordinates(
                self.cutter[-1], self.cutter[0])
            curr_sign_mul_vectors = self.compulate_sign_mul_vectors(
                vector_1, vector_2)
            if curr_sign_mul_vectors * sign_mul_vectors <= 0:
                flag = False

        return flag

    def cut_off_sutherland_hodgman(self, cutter, polygon):
        cutter.append(cutter[0])
        cutter.append(cutter[1])
        for i in range(len(cutter) - 2):
            new = []
            point_1 = polygon[0]
            if self.is_visible(point_1, cutter[i], cutter[i + 1], cutter[i + 2]):
                new.append(point_1)
            s = polygon[0]
            for j in range(1, len(polygon)):
                t = self.is_intersection(
                    [s, polygon[j]], [cutter[i], cutter[i + 1]], cutter[i + 2])
                if t:
                    new.append(t)
                s = polygon[j]
                if self.is_visible(s, cutter[i], cutter[i + 1], cutter[i + 2]):
                    new.append(s)

            if not len(new):
                return False

            t = self.is_intersection(
                [s, point_1], [cutter[i], cutter[i + 1]], cutter[i + 2])
            if t:
                new.append(t)
            polygon = deepcopy(new)

        return polygon

    def is_visible(self, point, cutter_point_1, cutter_point_2, cutter_point_3):
        flag_visible = True
        inner_normal = self.find_inner_normal(
            cutter_point_1, cutter_point_2, cutter_point_3)
        vector = self.get_vector_coordinates(cutter_point_2, point)
        if self.find_scalar(inner_normal, vector) < 0:
            flag_visible = False

        return flag_visible

    def is_intersection(self, input_edge, cutter_edge, next_cutter_point):
        visible_1 = self.is_visible(
            input_edge[0], cutter_edge[0], cutter_edge[1], next_cutter_point)
        visible_2 = self.is_visible(
            input_edge[1], cutter_edge[0], cutter_edge[1], next_cutter_point)

        if not (visible_1 ^ visible_2):
            return False

        inner_normal = self.find_inner_normal(
            cutter_edge[0], cutter_edge[1], next_cutter_point)

        D = self.find_directrise(input_edge[0], input_edge[1])
        W = self.find_w(input_edge[0], cutter_edge[0])

        D_scalar = self.find_scalar(D, inner_normal)
        W_scalar = self.find_scalar(W, inner_normal)

        t = -W_scalar / D_scalar

        param_point = self.convert_to_parametric(
            input_edge[0], input_edge[1], t)
        return param_point

    # Перевод уравнение отрезка в параметрическое
    def convert_to_parametric(self, point_1: Dot, point_2: Dot, t):
        def convert_axis(a, b, t):
            return a + (b - a + 1) * t
        return Dot(convert_axis(point_1.x, point_2.x, t),
                   convert_axis(point_1.y, point_2.y, t))

    def find_w(self, point_section_1: Dot, point_cutter: Dot):
        return [point_section_1.x - point_cutter.x, point_section_1.y - point_cutter.y]

    # Нахождение директрисы отрезка (задает его направление)
    def find_directrise(self, point_1: Dot, point_2: Dot):
        return [point_2.x - point_1.x, point_2.y - point_1.y]

    # Вычисление скалярного произведения векторов
    def find_scalar(self, vector_1, vector_2):
        return vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1]

    # Вычисление внутренней нормали вектора многоугольника (пропорционален текущему вектору отсекателя)
    def find_inner_normal(self, point_1: Dot, point_2: Dot, point_3: Dot):
        # нормаль > 0 - находится точка внутри отсекателя
        # нормаль < 0 - находится точка вне отсекателя
        vect = self.get_vector_coordinates(point_1, point_2)
        inner_normal = [1, 0] if vect[0] == 0 else [-vect[1] / vect[0], 1]
        vector_cutter = self.get_vector_coordinates(point_2, point_3)
        if self.find_scalar(inner_normal, vector_cutter) < 0:
            inner_normal = [-inner_normal[0], -inner_normal[1]]
        return inner_normal
