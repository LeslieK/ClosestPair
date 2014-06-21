import math

class Point2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def r(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def theta(self):
        return math.atan2(self.y / self.x)

    def distanceTo(self, that):
        dx = self.x - that.x
        dy = self.y - that.y
        return math.sqrt(dx * dx + dy * dy)

    def distanceSquaredTo(self, that):
        dx = self.x - that.x
        dy = self.y - that.y
        return dx * dx + dy * dy

    def __eq__(self, that):
        if id(self) == id(that):
            return True
        if that is None:
            return False
        if type(self) != type(that):
            return False
        if self.x != that.x:
            return False
        if self.y != that.y:
            return False
        return True

#################################### 
if __name__ == "__main__":
    x = Point2D(1.5, 0)
    y = Point2D(1.5, 2)
    z = x.distanceTo(y)

