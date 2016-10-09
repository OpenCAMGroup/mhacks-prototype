import gcode

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
    def __init__(self, positions, depth):
        self.positions = positions
        self.depth = depth
        return super().__init__()

    def printPolygon(self, initPoint = (0,0)):
        result = (gcode.Goto({'z': gcode.SAFE}, fast=True))
        result += ( gcode.Goto({'x': self.positions[0][0]+initPoint[0], 'y': self.positions[0][1]+initPoint[1]}, fast = True) )
        result += ( gcode.Goto({'z': -self.depth}, fast = False, feed = 50  ) )

        for pos in self.positions[1:]:
            result += ( gcode.Goto({'x': pos[0]+initPoint[0], 'y': pos[1]+initPoint[1]}, fast = False) )
            
        result += (gcode.Goto({'z': gcode.SAFE}, fast = False))
        result += (gcode.Goto({'z': gcode.SAFE}, fast=True))
        return result

class Drill(Geometry):
    def __init__(self, cutDepth):
        self.cutDepth = cutDepth
        return super().__init__()

    def printDrills(self, positions):
        result = (gcode.Goto({'z': gcode.SAFE}, fast=True) + gcode.Spindle(True))

        # Assuming G90 (absolute positioning)
        for pos in positions:
            result += gcode.Goto({'x': pos[0], 'y': pos[1]}, fast=True)
            result += gcode.Goto({'z': -self.cutDepth}, fast=False)
            result += gcode.Goto({'z': gcode.SAFE}, fast=False)

        result += gcode.Spindle(False)
        return result