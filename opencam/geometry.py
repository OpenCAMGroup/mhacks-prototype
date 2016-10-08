class Geometry:
    def __init__(self):
        return

class Line(Geometry):
    def __init__(self, vect = [0,0]):
        self.vect = vect
        return super().__init__()

class Circle(Geometry):
    def __init__(self, radius = 0):
        self.radius = radius
        return super().__init__()