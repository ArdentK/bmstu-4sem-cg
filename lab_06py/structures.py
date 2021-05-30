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


class Polygon:
    def __init__(self):
        self.vertices: list[Dot] = []
        self.extrema: list[int] = []

    def add_vertex(self, vertex: Dot):
        self.vertices.append(vertex)

        if self.size() > 2:
            self.update_extrema()

    def update_extrema(self):
        vert, curr_index = self.vertices, len(self.vertices) - 2
        if vert[curr_index].y == min([p.y for p in vert[-3:]]) \
                or vert[curr_index].y == max([p.y for p in vert[-3:]]):
            self.extrema.append(curr_index)

    def is_closed(self):
        return len(self.vertices) > 1 and (self.vertices[0]
                                           == self.vertices[-1])

    def close(self):
        self.add_vertex(self.vertices[0])

    def size(self):
        return len(self.vertices)


class Figure:
    def __init__(self):
        self.data: list[Polygon] = [Polygon()]
        self.p_min = Dot(10000, 10000)
        self.p_max = Dot(-10, -10)

    def is_empty(self):
        return len(self.data) == 1 and self.data[-1].size() == 0

    def clear(self):
        self.p_min = Dot(100000, 100000)
        self.p_max = Dot(-100000, -100000)
        self.data = [Polygon()]

    def add_polygon(self):
        self.data.append(Polygon())

    def add_vertex(self, vertex):
        self.p_max.x = max(vertex.x, self.p_max.x)
        self.p_max.y = max(vertex.y, self.p_max.y)

        self.p_min.x = min(vertex.x, self.p_min.x)
        self.p_min.y = min(vertex.y, self.p_min.y)

        self.data[-1].add_vertex(vertex)

    def close_this_polygon(self):
        self.data[-1].close()
        self.add_polygon()
