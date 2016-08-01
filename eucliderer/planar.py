#!/usr/bin/env python
import operator

class Camera:
    def __init__(self, position=(0,0), size=(100,100), field=(1,1)):
        self.position = position
        self.size = size
        self.field = field

        self._calc_boundaries()
    def move(self, position):
        self.position = position
        self._calc_boundaries()
    def shift(self, delta):
        self.position = map(operator.add, self.position, delta)
        self._calc_boundaries()
    def resize(self, size):
        self.size = size
        self._calc_boundaries()
    def fov(self, field):
        self.field = field
        self._calc_boundaries()
    def _calc_boundaries(self):
        self.left = self.position[0]
        self.right = self.position[0] + self.field[0]
        self.down = self.position[1]
        self.top = self.position[1] + self.field[1]
        self.left_segment = Line(Point((self.left, self.down)), Point((self.left, self.top)))
        self.right_segment = Line(Point((self.right, self.down)), Point((self.right, self.top)))
        self.top_segment = Line(Point((self.left, self.top)), Point((self.right, self.top)))
        self.down_segment = Line(Point((self.left, self.down)), Point((self.right, self.down)))

class Point:
    def __init__(self, position, size=1, color=(1,1,1)):
        self.position = position
        self.size = size
        self.color = color
    def shift(self, delta):
        self.position = map(operator.add, self.position, delta)
    def __str__(self):
        return "Point @%s" % (self.position,)

class Renderer():
    def _point_inside(self, camera, point):
        if point.position[0] > camera.left \
            and point.position[0] < camera.right \
            and point.position[1] > camera.down \
            and point.position[1] < camera.top:
            return True
        else:
            return False

class PointsRenderer(Renderer):
    def render(self, buffer, camera, points):

        visible = [ point for point in points
                   if self._point_inside(camera, point) ]

        # import pdb; pdb.set_trace()
        horizontal_size = camera.right - camera.left
        vertical_size = camera.down - camera.top
        for point in visible:
            x = (point.position[0]-camera.left)*camera.size[0]/horizontal_size
            y = (point.position[1]-camera.top)*camera.size[1]/vertical_size

            rx = int(round(x))
            ry = int(round(y))
            for i in range( -point.size/2, point.size/2):
                for j in range( -point.size/2, point.size/2):
                    rxi = rx + i
                    ryj = ry + j
                    if rxi < 0 or rxi >= camera.size[0] or ryj < 0 or ryj >= camera.size[1]:
                        continue
                    buffer[rxi][ryj] = point.color

class Line:
    def __init__(self, begin, end, size=1, color=(1,1,1)):
        self.begin = begin
        self.end = end
        self.size = size
        self.color = color
    def __str__(self):
        return "Line from %s to %s" % (self.begin, self.end)
    def shift(self, delta):
        self.begin.shift(delta)
        self.end.shift(delta)

class DDALinesRenderer(Renderer):
    """
    http://www.tutorialspoint.com/computer_graphics/line_generation_algorithm.htm
    """
    def render(self, buffer, camera, lines):
        # inside = [ line for line in lines
        #           if self._point_inside(camera, line.begin)
        #              and self._point_inside(camera, line.end) ]
        inside = []
        begin = []
        end = []
        outside = []

        for line in lines:
            if self._point_inside(camera, line.begin):
                if self._point_inside(camera, line.end):
                    inside.append(line)
                else:
                    begin.append(line)
            else:
                if self._point_inside(camera, line.end):
                    end.append(line)
                else:
                    outside.append(line)

        # import pdb; pdb.set_trace()

        horizontal_size = camera.right - camera.left
        vertical_size = camera.down - camera.top
        for line in inside:
            x0 = (line.begin.position[0]-camera.left)*camera.size[0]/horizontal_size
            y0 = (line.begin.position[1]-camera.down)*camera.size[1]/vertical_size
            x1 = (line.end.position[0]-camera.left)*camera.size[0]/horizontal_size
            y1 = (line.end.position[1]-camera.down)*camera.size[1]/vertical_size

            dx = x1 - x0
            dy = y1 - y0

            steps = abs(dx if abs(dx) > abs(dy) else dy)
            xinc = dx/float(steps)
            yinc = dy/float(steps)

            for i in range(0, int(steps)):
                buffer[int(round(x0))][int(round(y0))] = line.color
                x0 += xinc
                y0 += yinc

    def _draw_buffer_line(self, buffer, begin, end):
        pass

class BresenhamLinesRenderer(Renderer):
    """
    http://members.chello.at/~easyfilter/bresenham.html
    """
    def render(self, buffer, camera, line):
        pass

class Planar():
    def __init__(self, size=(100,100)):
        self.camera = Camera( (0,0), size, (1,1))
        self._points = []
        self._lines = []
        self._point_renderer = PointsRenderer()
        self._line_renderer = DDALinesRenderer()
    def render(self, buffer):
        buffer[:,:] = (0, 0, 0)
        self._line_renderer.render(buffer, self.camera, self._lines)
        self._point_renderer.render(buffer, self.camera, self._points)
    def add_point(self, point):
        self._points.append(point)
    def add_points(self, points):
        self._points.extend(points)
    def add_line(self, line):
        self._lines.append(line)

if __name__=="__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    b = np.zeros( (1000, 1000, 3) )

    p = Planar( (1000, 1000) )

    p.add_point( Point( (0.2, 0.2), size=5, color=(0,0,1) ) )
    p.add_point( Point( (0.5, 0.5), size=5, color=(0,1,0) ) )
    p.add_point( Point( (1.5, 1.5), size=5, color=(1,0,0) ) )

    p.add_line( Line(Point((0.3, 0.1)), Point((1.1,1.4)), color=(0,0,1)) )
    p.add_line( Line(Point((0.9, 0.9)), Point((.1,.8)), color=(0,1,0)) )

    p.add_points( (Point((0.3, 0.1), size=9), Point((1.1,1.4), size=9)) )
    p.add_points( (Point((0.9, 0.9), size=9), Point((.1,.8), size=9)) )

    p.render(b)

    plt.imshow(b)
    plt.show()

    p.camera.move( (-1, -1) )
    p.camera.fov( (2, 2) )

    p.render(b)
    plt.imshow(b)
    plt.show()

    p.camera.move( (-1, -1) )
    p.camera.fov( (3, 3) )

    p.render(b)
    plt.imshow(b)
    plt.show()
