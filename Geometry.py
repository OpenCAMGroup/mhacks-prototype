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

def printStart():
    print("O1 Custom Built Program by OpenCAM")
    print("G90 G54;")

def printDrills(positions, cutDepth, toolHeight):
    # Assuming G90 (absolute positioning) and that Z1. is a safe position
    print("G43 H{} Z1.".format(toolHeight))
    print("G00 X{} Y{} S2000 M3;".format(positions[0][0], positions[0][1]))
    print("G01 Z{} F8;\nZ{};".format(-cutDepth-1, cutDepth+1))
    for x in range(1,len(positions)):
        print("G00 X{} Y{};\nG01 Z{};\nZ{};".format(positions[x][0], positions[x][1], -cutDepth-1, cutDepth+1))
    print("M05 G49 Z1.;")