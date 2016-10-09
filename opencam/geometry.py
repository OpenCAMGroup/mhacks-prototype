from . import gcode
from .command import Command

class Geometry(Command):
    pass

class Line(Geometry):
    def __init__(self, vect=(0,0)):
        super().__init__(self)
        self.vect = vect

    def compile(self, position):
        pass

class Circle(Geometry):
    def __init__(self, radius = 0):
        super().__init__(self)
        self.radius = radius

class Polygon(Geometry):
    def __init__(self, positions):
        super().__init__(self)
        self.positions = positions

    def printPolygon(self):
        result = (gcode.Goto({'z': gcode.SAFE}, fast=True) + gcode.Spindle(True))

        for pos in positions:
            result +=  gcode.Goto({'x': pos[0], 'y': pos[1]}, fast = False)

        result += (gcode.Goto({'z': gcode.SAFE}, fast=True) + gcode.Spindle(False))
        return result

class Drill(Geometry):
    def __init__(self, cutDepth):
        super().__init__(self)
        self.cutDepth = cutDepth

    def printDrills(self, positions, toolHeight):
        result = (gcode.Goto({'z': gcode.SAFE}, fast=True) + gcode.Spindle(True))

        # Assuming G90 (absolute positioning)
        for pos in positions:
            result += gcode.Goto({'x': pos[0], 'y': pos[1]}, fast=True)
            result += gcode.Goto({'z': -self.cutDepth}, fast=False)
            result += gcode.Goto({'z': gcode.SAFE}, fast=False)

        result += gcode.Spindle(False)
        return result
