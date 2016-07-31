#!/usr/bin/env python
import operator

class Camera:
    def __init__(self, position=(0,0), size=(100,100), field=(1,1)):
        self.position = position
        self.size = size
        self.field = field
    def move(self, position):
        self.position = position
    def shift(self, delta):
        self.position = map(operator.add, self._position, delta)
    def resize(self, size):
        self.size = size
    def field(self, field):
        self.field = field

class Point:
    def __init__(self, position, size=1, color=(1,1,1)):
        self.position = position
        self.size = size
        self.color = color

class PointsRenderer():
    def render(self, buffer, camera, points):
        left = camera.position[0]
        right = camera.field[0]
        down = camera.position[1]
        top = camera.field[1]

        visible = [ point for point in points
                    if point.position[0] > left
                      and point.position[0] < right
                      and point.position[1] > down
                      and point.position[1] < top ]

        # import pdb; pdb.set_trace()

        for point in visible:
            print camera.size
            print point.position[0],
            x = (point.position[0] - left)/(right - left)
            print x,
            x = int(round(abs(x)*camera.size[0]))
            print x
            print point.position[1],
            y = (point.position[1] - down)/(top - down)
            print y,
            y = int(round(abs(y)*camera.size[1]))
            print y
            # import pdb; pdb.set_trace()
            buffer[x,y] = point.color

class Line:
    def __init__(self, position, size=1, color=(1,1,1)):
        self._position = position
        self._size = size
        self._color = color

class DDALinesRenderer():
    def render(self, buffer, camera, line):
        pass

class BresenhamLinesRenderer():
    def render(self, buffer, camera, line):
        pass

class Planar():
    def __init__(self):
        self._camera = Camera( (0,0), (100, 100), (1,1))
        self._points = []
        self._lines = []
        self._point_renderer = PointsRenderer()
        self._line_renderer = DDALinesRenderer()
    def render(self, buffer):
        self._point_renderer.render(buffer, self._camera, self._points)
        self._line_renderer.render(buffer, self._camera, self._lines)
    def add_point(self, point):
        self._points.append(point)
    def add_points(self, points):
        self._points.extend(points)

if __name__=="__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    b = np.zeros( (100, 100, 3) )
    p = Planar()
    p.add_point( Point( (0.2, 0.2) ) )
    p.add_point( Point( (0.5, 0.5) ) )
    p.add_point( Point( (1.5, 1.5) ) )

    p.render(b)

    plt.imshow(b)
    plt.show()
