from timeit import timeit

from structures import Dot

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtGui import QColor, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMessageBox

eps = 5

MASK_LEFT = 0b0001
MASK_RIGHT = 0b0010
MASK_DOWN = 0b0100
MASK_UP = 0b1000

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sections = []
        self.cutter = None
        self.cutter_points = [0, 0, 0, 0]
        self.last_cutter_vertex = None
        self.last_point = None

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
        self.cutter = None
        self.last_cutter_vertex = None
        self.last_point = None

    def mousePressEvent(self, event):
        position = Dot(event.pos().x(), event.pos().y())
        if self.ui.QRB_cutter.isChecked():
            if event.buttons() == Qt.LeftButton:
                self.add_cutter(position)
        elif self.ui.QRB_section.isChecked():
            if event.buttons() == Qt.LeftButton:
                exactly = QApplication.keyboardModifiers() & Qt.ControlModifier
                self.add_section(position, exactly=exactly)

    def get_curr_color(self):
        color_text = self.ui.QCB_color.currentText()

        if (color_text == "Белый(фон)"):
            color = Qt.white
        elif (color_text == "Черный"):
            color = Qt.black
        elif (color_text == "Синий"):
            color = Qt.blue

        return color

    def set_cutter_point(self):
        self.cutter_points[LEFT] = min(
            self.cutter[0].x, self.cutter[1].x, self.cutter[2].x, self.cutter[3].x)
        self.cutter_points[RIGHT] = max(
            self.cutter[0].x, self.cutter[1].x, self.cutter[2].x, self.cutter[3].x)
        self.cutter_points[UP] = min(
            self.cutter[0].y, self.cutter[1].y, self.cutter[2].y, self.cutter[3].y)
        self.cutter_points[DOWN] = max(
            self.cutter[0].y, self.cutter[1].y, self.cutter[2].y, self.cutter[3].y)

    def add_section_by_btn(self):
        p1 = Dot(self.ui.QSB_section_x_start.value(),
                 self.ui.QSB_section_y_start.value())
        p2 = Dot(self.ui.QSB_section_x_end.value(),
                 self.ui.QSB_section_y_end.value())

        self.sections.append([p1, p2])

        qp = QPainter(self.image)
        qp.setPen(QPen(self.get_curr_color(), 1))
        qp.drawLine(self.sections[-1][0].to_qpoint(),
                    self.sections[-1][1].to_qpoint())
        qp.end()

        self.image_set()

    def add_cutter_by_btn(self):
        p1 = Dot(self.ui.QSB_cutter_x_start.value(),
                 self.ui.QSB_cutter_y_start.value())
        p3 = Dot(self.ui.QSB_cutter_x_end.value(),
                 self.ui.QSB_cutter_y_end.value())
        p2 = Dot(p1.x, p3.y)
        p4 = Dot(p3.x, p1.y)

        if self.cutter != None:
            self.del_old_cutter()

        self.cutter = [p1, p4, p3, p2]
        self.set_cutter_point()

        self.paint_cutter()

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

            if self.cutter:
                dx1 = abs(pos.x - self.cutter_points[LEFT])
                dy1 = abs(pos.y - self.cutter_points[DOWN])
                dx2 = abs(pos.x - self.cutter_points[RIGHT])
                dy2 = abs(pos.y - self.cutter_points[UP])

                if (dx1 < eps):
                    pos.x = self.cutter_points[LEFT]
                elif (dx2 < eps):
                    pos.x = self.cutter_points[RIGHT]
                if dy1 < eps:
                    pos.y = self.cutter_points[DOWN]
                elif dy2 < eps:
                    pos.y = self.cutter_points[UP]

            self.sections.append([self.last_point, pos])

            qp = QPainter(self.image)
            qp.setPen(QPen(self.get_curr_color(), 1))
            qp.drawLine(self.sections[-1][0].to_qpoint(),
                        self.sections[-1][1].to_qpoint())
            qp.end()

            self.image_set()

            self.last_point = None

    def paint_cutter(self):
        qp = QPainter(self.image)
        qp.setPen(QPen(Qt.red, 1))
        qp.drawLine(self.cutter[0].to_qpoint(), self.cutter[1].to_qpoint())
        qp.drawLine(self.cutter[1].to_qpoint(), self.cutter[2].to_qpoint())
        qp.drawLine(self.cutter[2].to_qpoint(), self.cutter[3].to_qpoint())
        qp.drawLine(self.cutter[3].to_qpoint(), self.cutter[0].to_qpoint())
        qp.end()
        self.image_set()

    def del_old_cutter(self):
        self.image_init()
        self.image_set()
        self.cutter.clear()
        self.cutter = None
        qp = QPainter(self.image)
        qp.setPen(QPen(self.get_curr_color(), 1))
        for i in range(len(self.sections)):
            qp.drawLine(self.sections[i][0].to_qpoint(),
                        self.sections[i][1].to_qpoint())
        qp.end()
        self.image_set()

    def add_cutter(self, pos: Dot):
        if self.last_cutter_vertex == None:
            self.last_cutter_vertex = pos
        else:
            if self.cutter != None:
                self.del_old_cutter()

            point_3 = Dot(self.last_cutter_vertex.x, pos.y)
            point_4 = Dot(pos.x, self.last_cutter_vertex.y)

            self.cutter = [self.last_cutter_vertex, point_4, pos, point_3]

            self.paint_cutter()

            self.set_cutter_point()

            self.last_cutter_vertex = None

            self.image_set()

    # Создать четырехразрядный код концов отрезка
    def create_segment_bits(self, segment_point):
        segment_bits = 0b0000
        if segment_point.x < self.cutter_points[LEFT]:
            segment_bits |= MASK_LEFT
        if segment_point.x > self.cutter_points[RIGHT]:
            segment_bits |= MASK_RIGHT
        if segment_point.y > self.cutter_points[DOWN]:
            segment_bits |= MASK_DOWN
        if segment_point.y < self.cutter_points[UP]:
            segment_bits |= MASK_UP

        return segment_bits

    # Поиск вертикальных линий
    def find_vertical(self, segment, current_index, rectangle):
        if segment[current_index].y < self.cutter_points[UP]:
            return Dot(segment[current_index].x, self.cutter_points[UP])
        elif segment[current_index].y > self.cutter_points[DOWN]:
            return Dot(segment[current_index].x, self.cutter_points[DOWN])
        else:
            return segment[current_index]

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

        if self.cutter == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не был введен отсекатель")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return

        for i in range(len(self.sections)):
            self.cut_section(self.sections[i])

    def cut_section(self, section):
        section_bits_points = []
        section_bits_points.append(self.create_segment_bits(section[0]))
        section_bits_points.append(self.create_segment_bits(section[1]))

        # отрезок полностью невидим
        if section_bits_points[0] & section_bits_points[1]:
            return

        # отрезок полностью видим
        if section_bits_points[0] == 0 and section_bits_points[1] == 0:
            self.draw_part_segment(section, Qt.black)
            return

        curr_index_point = 0
        result_points = []

        # проверка видимости первой вершины
        if section_bits_points[0] == 0:
            curr_index_point = 1
            result_points.append(section[0])

        # проверка видимости второй вершины
        if section_bits_points[1] == 0:
            curr_index_point = 1
            result_points.append(section[1])
            section_bits_points.reverse()
            section.reverse()

        while curr_index_point < 2:
            if section[0].x == section[1].x:
                result_points.append(self.find_vertical(
                    section, curr_index_point, self.cutter))
                curr_index_point += 1
                continue

            m = (section[1].y - section[0].y) / (section[1].x - section[0].x)

            if section_bits_points[curr_index_point] & MASK_LEFT:
                y = round(
                    m * (self.cutter_points[LEFT] - section[curr_index_point].x) + section[curr_index_point].y)
                if y <= self.cutter_points[DOWN] and y >= self.cutter_points[UP]:
                    result_points.append(Dot(self.cutter_points[LEFT], y))
                    curr_index_point += 1
                    continue
            elif section_bits_points[curr_index_point] & MASK_RIGHT:
                y = round(
                    m * (self.cutter_points[RIGHT] - section[curr_index_point].x) + section[curr_index_point].y)
                if y <= self.cutter_points[DOWN] and y >= self.cutter_points[UP]:
                    result_points.append(Dot(self.cutter_points[RIGHT], y))
                    curr_index_point += 1
                    continue

            if m == 0:
                curr_index_point += 1
                continue

            if section_bits_points[curr_index_point] & MASK_UP:
                x = round(
                    (self.cutter_points[UP] - section[curr_index_point].y) / m + section[curr_index_point].x)
                if x >= self.cutter_points[LEFT] and x <= self.cutter_points[RIGHT]:
                    result_points.append(Dot(x, self.cutter_points[UP]))
                    curr_index_point += 1
                    continue
            elif section_bits_points[curr_index_point] & MASK_DOWN:
                x = round(
                    (self.cutter_points[DOWN] - section[curr_index_point].y) / m + section[curr_index_point].x)
                if x >= self.cutter_points[LEFT] and x <= self.cutter_points[RIGHT]:
                    result_points.append(Dot(x, self.cutter_points[DOWN]))
                    curr_index_point += 1
                    continue

            curr_index_point += 1

        if result_points != [] and len(result_points) > 1:
            self.draw_part_segment(result_points, Qt.black)
