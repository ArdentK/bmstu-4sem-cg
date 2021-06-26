from structures import Dot
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtGui import QColor, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMessageBox


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.cutter = []
        self.sections_color = Qt.blue
        self.cutter_color = Qt.red
        self.sections = []
        self.last_point = None
        self.flag_locked_cutter = False

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
        self.sections.clear()
        self.cutter.clear()
        self.last_point = None

    def mousePressEvent(self, event):
        position = Dot(event.pos().x(), event.pos().y())
        if self.ui.QRB_cutter.isChecked():
            if event.buttons() == Qt.LeftButton:
                exactly = QApplication.keyboardModifiers() & Qt.ControlModifier
                self.add_cutter(position, exactly)
            elif event.buttons() == Qt.RightButton:
                self.close_poly()
        elif self.ui.QRB_section.isChecked():
            if event.buttons() == Qt.LeftButton:
                exactly = QApplication.keyboardModifiers() & Qt.ControlModifier
                self.add_section(position, exactly=exactly)

    def add_section_by_btn(self):
        p1 = Dot(self.ui.QSB_section_x_start.value(),
                 self.ui.QSB_section_y_start.value())
        p2 = Dot(self.ui.QSB_section_x_end.value(),
                 self.ui.QSB_section_y_end.value())

        self.sections.append([p1, p2])

        qp = QPainter(self.image)
        qp.setPen(QPen(self.sections_color, 1))
        qp.drawLine(self.sections[-1][0].to_qpoint(),
                    self.sections[-1][1].to_qpoint())
        qp.end()

        self.image_set()

    def add_section(self, pos: Dot, exactly=False):
        if self.last_point == None:
            self.last_point = pos
        else:
            if exactly:
                dx, dy = abs(
                    pos.x - self.last_point.x), abs(pos.y - self.last_point.y)
                if dx < dy:
                    pos.x = self.last_point.x
                else:
                    pos.y = self.last_point.y

            self.sections.append([self.last_point, pos])

            qp = QPainter(self.image)
            qp.setPen(QPen(self.sections_color, 1))
            qp.drawLine(self.sections[-1][0].to_qpoint(),
                        self.sections[-1][1].to_qpoint())
            qp.end()

            self.image_set()

            self.last_point = None

    def add_cutter(self, pos: Dot, exactly=False):
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

    def close_poly(self):
        if len(self.cutter) < 3:
            return

        qp = QPainter(self.image)
        qp.setPen(QPen(self.cutter_color, 1))
        self.flag_locked_cutter = True
        qp.drawLine(self.cutter[-1].to_qpoint(),
                    self.cutter[0].to_qpoint())
        qp.end()

        self.image_set()

    # Отрисовка части отрезка
    def draw_part_segment(self, result_points, colour_result):
        qp = QPainter(self.image)
        qp.setPen(QPen(colour_result, 2))
        qp.drawLine(result_points[0].to_qpoint(),
                    result_points[1].to_qpoint())
        qp.end()

        self.image_set()

    def cut_all_sections(self):
        if self.sections == []:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не были введены отрезки")
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

        for i in range(len(self.sections)):
            self.cut_section(self.sections[i])

    def get_vector_coordinates(self, point_1: Dot, point_2: Dot):
        return [point_2.x - point_1.x, point_2.y - point_1.y]

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

    # Нахождение директрисы отрезка (задает его направление)
    def find_directrise(self, point_1: Dot, point_2: Dot):
        return [point_2.x - point_1.x, point_2.y - point_1.y]

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

    # Вычисление скалярного произведения векторов
    def find_scalar(self, vector_1, vector_2):
        return vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1]

    def find_w(self, point_section_1: Dot, point_cutter: Dot):
        return [point_section_1.x - point_cutter.x, point_section_1.y - point_cutter.y]

    # Перевод уравнение отрезка в параметрическое
    def convert_to_parametric(self, point_1: Dot, point_2: Dot, t):
        def convert_axis(a, b, t):
            return a + (b - a) * t
        return Dot(convert_axis(point_1.x, point_2.x, t),
                   convert_axis(point_1.y, point_2.y, t))

    # Выполнить отсечение каждого отрезка (алгоритм Кируса-Бека)
    def cut_section(self, section):
        len_cutter = len(self.cutter)
        t_down = 0
        t_up = 1
        D = self.find_directrise(section[0], section[1])

        for i in range(len_cutter):
            el1, el2, el3 = None, None, None

            if i < len_cutter - 2:
                el1 = self.cutter[i]
                el2 = self.cutter[i + 1]
                el3 = self.cutter[i + 2]
            elif i == len_cutter - 2:
                el1 = self.cutter[-2]
                el2 = self.cutter[-1]
                el3 = self.cutter[0]
            elif i == len_cutter - 1:
                el1 = self.cutter[-1]
                el2 = self.cutter[0]
                el3 = self.cutter[1]

            inner_normal = self.find_inner_normal(el1, el2, el3)

            W = self.find_w(section[0], self.cutter[i])
            D_scalar = self.find_scalar(D, inner_normal)
            W_scalar = self.find_scalar(W, inner_normal)

            # отрезок невидим
            if D_scalar == 0 and W_scalar <= 0:
                return

            if D_scalar == 0:
                param_point_1 = self.convert_to_parametric(
                    section[0], section[1], t_down)
                self.draw_part_segment(
                    [param_point_1, param_point_1], Qt.black)
                return

            t = -W_scalar / D_scalar

            if D_scalar > 0:
                if t > 1:
                    # отрезок невидим
                    return
                else:
                    t_down = max(t_down, t)
            elif D_scalar < 0:
                if t < 0:
                    # отрезок невидим
                    return
                else:
                    t_up = min(t_up, t)

        if t_down <= t_up:
            param_point_1 = self.convert_to_parametric(
                section[0], section[1], t_down)
            param_point_2 = self.convert_to_parametric(
                section[0], section[1], t_up)
            self.draw_part_segment(
                [param_point_1, param_point_2], Qt.black)

        return
