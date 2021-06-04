from timeit import timeit

from line_algos import dda
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
        self.seed = Dot(0, 0)

    def image_init(self):
        self.image = QImage(self.width(), self.height(),
                            QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)

    def set_table(self, table: DataTable):
        self.table = table

    def set_ui(self, ui):
        self.ui = ui

    def image_set(self):
        self.pixmap = QPixmap().fromImage(self.image)
        self.setPixmap(self.pixmap)

    def clear(self):
        self.figure.clear()
        self.image_init()
        self.image_set()

    def mousePressEvent(self, event):
        position = Dot(event.pos().x(), event.pos().y())
        if self.ui.QRB_seeding_point.isChecked():
            self.set_seeding_dot(position)
        else:
            if event.buttons() == Qt.LeftButton:
                exactly = QApplication.keyboardModifiers() & Qt.ControlModifier
                self.add_dot(position, exactly=exactly)
                self.table.add_dot(position)
            elif event.buttons() == Qt.RightButton:
                self.close_poly()

    def mouseMoveEvent(self, event):
        if self.ui.QRB_figure.isChecked():
            position = Dot(event.pos().x(), event.pos().y())
            if event.buttons() == Qt.LeftButton:
                exactly = QApplication.keyboardModifiers() & Qt.ControlModifier
                self.add_dot(position, exactly=exactly)

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

    def set_seeding_dot(self, dot: Dot):
        self.seed = dot
        self.ui.QL_seed.setText(
            "Затравочная точка: (" + str(dot.x) + "," + str(dot.y) + ")")
        self.ui.QL_seed.adjustSize()

        color = self.get_curr_color()
        result = None
        if self.ui.QCB_delay.isChecked():
            self.ui.canvas.fill(dot, color, True)
        else:
            result = timeit(lambda: self.ui.canvas.fill(dot, color),
                            number=1) * 1000
            self.time_info(result)

    def time_info(self, time):
        if time is not None:
            text = f'Время закраски: {round(time, 2)} мс'
        else:
            text = f'Время закраски: None'
        QtWidgets.QMessageBox.about(self, "Время", text)

    def add_dot(self, pos: Dot, exactly=False):
        if exactly and self.figure.data[-1].size():
            last_vertex = self.figure.data[-1].vertices[-1]
            dx, dy = abs(pos.x - last_vertex.x), abs(pos.y - last_vertex.y)
            if dx < dy:
                pos.x = last_vertex.x
            else:
                pos.y = last_vertex.y

        self.figure.add_vertex(pos)
        # self.table.add_dot(pos)

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

    def border_fill(self):
        dda(self.image, Dot(0, 0), Dot(0, self.image.height() - 1))
        dda(self.image, Dot(0, 0), Dot(self.image.width() - 1, 0))
        dda(self.image, Dot(0, self.image.height() - 1),
            Dot(self.image.width() - 1, self.image.height() - 1))
        dda(self.image, Dot(self.image.width() - 1, 0),
            Dot(self.image.width() - 1, self.image.height() - 1))

    def cmp_pix(self, pixel: Dot, cmp: QColor):
        return self.image.pixelColor(pixel.to_qpoint()) == cmp

    def set_pix(self, pixel: Dot, cmp: QColor) -> None:
        self.image.setPixelColor(pixel.to_qpoint(), cmp)

    def fill(self, seed: Dot, color: QColor, delay=False):
        stack = []
        stack.append(seed)
        self.border_fill()
        # return
        while stack:
            p_curr = stack.pop()
            self.set_pix(p_curr, color)
            tmp_x = p_curr.x
            p_curr.x += 1

            while not self.cmp_pix(p_curr, Qt.black):
                self.set_pix(p_curr, color)
                p_curr.x += 1

            rx = p_curr.x - 1
            p_curr.x = tmp_x
            p_curr.x -= 1

            while not self.cmp_pix(p_curr, Qt.black):
                self.set_pix(p_curr, color)
                p_curr.x -= 1

            lx = p_curr.x + 1
            p_curr.x = tmp_x
            tmp_y = p_curr.y

            for i in (1, -1):
                p_curr.x = lx
                p_curr.y = tmp_y + i

                while p_curr.x <= rx:
                    flag = False
                    while not self.cmp_pix(
                            p_curr, Qt.black) and not self.cmp_pix(
                                p_curr, color) and p_curr.x <= rx:
                        p_curr.x += 1
                        flag = True

                    if flag:
                        x, y = p_curr.x, p_curr.y
                        if p_curr.x != rx or self.cmp_pix(
                                p_curr, Qt.black) or self.cmp_pix(
                                    p_curr, color):
                            x -= 1
                        stack.append(Dot(x, y))

                    x_input = p_curr.x
                    while (self.cmp_pix(p_curr, Qt.black)
                           or self.cmp_pix(p_curr, color)) and p_curr.x <= rx:
                        p_curr.x += 1

                    if p_curr.x == x_input:
                        p_curr.x += 1
            if delay:
                QtWidgets.QApplication.processEvents(QEventLoop.AllEvents)
                self.image_set()

        self.image_set()
