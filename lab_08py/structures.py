from typing import Tuple

from PyQt5.QtCore import QPoint


class Dot():
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    @property
    def value(self) -> Tuple[float, float]:
        return self.x, self.y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    def to_qpoint(self):
        return QPoint(*self.value)
