class Circle:
    def __init__(self, x, y, radius):
        self.radius = radius
        self.x = x
        self.y = y
    def contains(self, point):
        dist2 = (self.x - point.x) ** 2 + (self.y - point.y) ** 2
        return dist2 <= self.radius ** 2

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

if __name__ == '__main__':
    x, y, r = map(int, input().split())
    circle = Circle(x, y, r)
    x, y = map(int, input().split())
    point = Point(x, y)
    print(circle.contains(point))