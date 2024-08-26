# 1. Реалізувати метод square в фігурах які
# залишилися.(Triangle + Parallelogram).
# Triangle - треба створити клас

from math import sin, pi

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Shape:  # class Shape(object)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0


class Circle(Shape):

    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def square(self):
        return pi * self.radius ** 2

    def __contains__ (self, point):
        dist2 = (self.x - point.x) ** 2 + (self.y - point.y) ** 2
        return dist2 <= self.radius ** 2


class Rectangle(Shape):

    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return self.width * self.height


class Parallelogram(Rectangle):

    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width)
        self.angle = angle

    def square(self):
        return self.width * self.height * sin(self.angle)

    def print_angle(self):
        print(self.angle)

    def __str__(self):
        result = super().__str__()
        return result + f'\nParallelogram: {self.width}, {self.height}, {self.angle}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Triangle(Parallelogram):
    def __init__(self, x, y, height, width, angle):
        super().__init__(self, x, y, height, width, angle)

    def square(self):
        return 0.5 * self.width * self.height * sin(self.angle)

class Scene:
    def __init__(self):
        self._figures = []

    def add_figure(self, figure):
        self._figures.append(figure)

    def total_square(self):
        return sum(f.square() for f in self._figures)

    def __str__(self):
        pass


if __name__ == '__main__':
    r = Rectangle(0, 0, 10, 20)
    r1 = Rectangle(10, 0, -10, 20)
    r2 = Rectangle(0, 20, 100, 20)

    c = Circle(10, 0, 10)
    c1 = Circle(100, 100, 5)

    p = Parallelogram(1, 2, 20, 30, 45)
    print(p.x)
    p1 = Parallelogram(1, 2, 20, 30, 45)
    print(str(p1))

    scene = Scene()
    scene.add_figure(r)
    scene.add_figure(r1)
    scene.add_figure(r2)
    scene.add_figure(c)
    scene.add_figure(c1)

    scene.total_square()

    # 2. реалізувати через in.

    print(Point(1, 2) in Circle(1, 2, 10))
    print(p1 in c1)