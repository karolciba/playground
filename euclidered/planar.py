import operator

class Camera:
    def __init__(self, position=(0.5,0.5), size=(100,100), field=(1,1)):
        self._position = position
        self._size = size
        self._field = field
    def move(self, position):
        self._position = position
    def shift(self, delta):
        self._position = map(operator.add, self_position, delta)
    def resize(self, size):
        self._size = size
    def field(self, field):
        self._field = field

class Point:
    def __init__(self, position, size=1, color=(1,1,1)):
        self._position = position
        self._size = size
        self._color = color

class PointRenderer():
    def render(self, buffer, camera, point):
        pass

class Line:
    def __init__(self, position, size=1, color=(1,1,1)):
        self._position = position
        self._size = size
        self._color = color

class DDALineRenderer():
    def render(self, buffer, camera, line):
        pass

class BresenhamLineRenderer():
    def render(self, buffer, camera, line):
        pass

class Planar():
    def __init__():
        self._camera = Camera( (0.5,0.5), (100, 100), (1,1))
        self._points = []
        self._lines = []
        self._point_renderer = PointRendere()
        self._line_renderer = DDALineRenderer()
    def render(buffer):
        for point in self._points:
            self._point_renderer.render(buffer, self._camera, point)
        for line in self._lines:
            self._line_renderer.render(buffer, self._camera, line)


if __name__=="__main__":
    print "hello"
