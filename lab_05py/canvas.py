from line_algos import dda, round
from structures import Dot, Figure

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtGui import QColor, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget


class DataTable(QtWidgets.QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def add_dot(self, dot):
        curr_row = self.rowCount()
        self.insertRow(curr_row)

        self.setItem(curr_row, 0, QtWidgets.QTableWidgetItem(str(dot.x)))
        self.setItem(curr_row, 1, QtWidgets.QTableWidgetItem(str(dot.y)))

    def clear(self) -> None:
        self.setRowCount(0)


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.figure = Figure()

    def image_init(self):
        self.image = QImage(self.width(), self.height(),
                            QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)

    def set_table(self, table: DataTable):
        self.table = table

    def image_set(self):
        self.pixmap = QPixmap().fromImage(self.image)
        self.setPixmap(self.pixmap)

    def clear(self):
        self.figure.clear()
        self.image_init()
        self.image_set()

    def mousePressEvent(self, event):
        position = Dot(event.pos().x(), event.pos().y())
        if event.buttons() == Qt.LeftButton:
            exactly = QApplication.keyboardModifiers() & Qt.ControlModifier
            self.add_dot(position, exactly=exactly)
        elif event.buttons() == Qt.RightButton:
            self.close_poly()

    def add_dot(self, pos: Dot, exactly=False):
        if exactly and self.figure.data[-1].size():
            last_vertex = self.figure.data[-1].vertices[-1]
            dx, dy = abs(pos.x - last_vertex.x), abs(pos.y - last_vertex.y)
            if dx < dy:
                pos.x = last_vertex.x
            else:
                pos.y = last_vertex.y

        self.figure.add_vertex(pos)
        self.table.add_dot(pos)

        qp = QPainter(self.image)
        qp.setPen(QPen(Qt.black, 4))
        # qp.drawEllipse(pos.to_qpoint(), 2, 2)
        last_poly = self.figure.data[-1]
        if last_poly.size() > 1:
            dda(self.image, last_poly.vertices[-2], last_poly.vertices[-1])
        qp.end()

        self.image_set()

    def close_poly(self):
        last_poly = self.figure.data[-1]
        if last_poly.size() < 3:
            return

        qp = QPainter(self.image)
        qp.setPen(QPen(Qt.black, 1))
        self.figure.close_this_polygon()
        dda(self.image, last_poly.vertices[-2], last_poly.vertices[-1])
        qp.end()

        self.image_set()

    def fill(self, color: QColor, delay=False):
        self.delay = delay
        self.image_init()
        self.outline()

        p_min, p_max = self.figure.p_min, self.figure.p_max
        mark_color = Qt.black
        bg_color = Qt.white
        figure_color = color
        curr_color = bg_color

        def change_color(c):
            return bg_color if (c == figure_color) else figure_color

        for y in range(p_max.y, p_min.y - 1, -1):
            for x in range(p_min.x, p_max.x + 1, 1):
                if self.image.pixelColor(x, y) == mark_color:
                    curr_color = change_color(curr_color)

                self.image.setPixelColor(x, y, curr_color)

            if delay:
                QtWidgets.QApplication.processEvents(QEventLoop.AllEvents)
                self.image_set()

        self.borders_and_points()
        self.image_set()

    def outline(self):
        polygons = self.figure.data

        for poly in polygons:
            vertices, length = poly.vertices, len(poly.vertices)
            extrema = poly.extrema

            for i in range(length):
                self.segment(vertices[i], vertices[(i + 1) % length],
                             [i in extrema, (i + 1) % length in extrema])

    def segment(self, p0: Dot, p1: Dot, is_extremum):
        if p0.y == p1.y:
            return

        if p0.y > p1.y:
            p0, p1 = p1, p0
            is_extremum.reverse()

        dy, dx = 1, (p1.x - p0.x) / (p1.y - p0.y)
        curr_p = Dot(p0.x, p0.y)
        mark_color = Qt.black

        while curr_p.y < p1.y:
            if self.image.pixelColor(int(curr_p.x + 0.5), int(curr_p.y)) != mark_color:
                self.image.setPixelColor(
                    int(curr_p.x + 0.5), int(curr_p.y), mark_color)
            else:
                self.image.setPixelColor(
                    int(curr_p.x + 0.5), int(curr_p.y), Qt.white)

            if self.delay:
                QtWidgets.QApplication.processEvents(QEventLoop.AllEvents)
                self.image_set()

            curr_p.x += dx
            curr_p.y += dy

    def borders_and_points(self):
        qp = QPainter(self.image)
        qp.setPen(QPen(Qt.black, 2))

        for poly in self.figure.data:
            vert = poly.vertices
            for i in range(len(vert) - 1):
                dda(self.image, vert[i], vert[i+1])
                qp.drawEllipse(vert[i].to_qpoint(), 1, 1)

        qp.end()
