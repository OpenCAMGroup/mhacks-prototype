from . import gcode

class Geometry:
    def __init__(self):
        return

class Line(Geometry):
    def __init__(self, vect=[0,0]):
        self.vect = vect
        return super().__init__()

class Circle(Geometry):
    def __init__(self, radius = 0):
        self.radius = radius
        return super().__init__()

class Polygon(Geometry):
    def __init__(self, positions):
        self.positions = positions
        return super().__init__()

    def printPolygon(self):
        result = (gcode.Goto({'z': gcode.SAFE}, fast=True) + gcode.Spindle(True))

        for pos in positions:
            result +=  gcode.Goto({'x': pos[0], 'y': pos[1]}, fast = False)

        result += (gcode.Goto({'z': gcode.SAFE}, fast=True) + gcode.Spindle(False))

class Drill(Geometry):
    def __init__(self, cutDepth):
        self.cutDepth = cutDepth
        return super().__init__()

    def printDrills(self, positions, toolHeight):
        result = (gcode.Goto({'z': gcode.SAFE}, fast=True) + gcode.Spindle(True))

        # Assuming G90 (absolute positioning)
        for pos in positions:
            result += gcode.Goto({'x': pos[0], 'y': pos[1]}, fast=True)
            result += gcode.Goto({'z': -self.cutDepth}, fast=False)
            result += gcode.Goto({'z': gcode.SAFE}, fast=False)

        result += gcode.Spindle(False)
        return result
