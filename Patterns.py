class Pattern:
    def __init__(self, geometry = None, initialPoint = [0,0]):
        self.initialPoint = initialPoint
        self.positions = []
        self.geometry = geometry

class RegularLinearPattern(Pattern):
    def __init__(self, *args):
        if isinstance(args[0], Pattern):
            pattern      = args[0]
            geometry     = pattern.geometry
            initialPoint = pattern.initialPoint
            numPoints    = args[1]
            spacing      = args[2]
            super().__init__(geometry, initialPoint)
            tempPos = [initialPoint]
            tempPos.extend(pattern.positions)
            for pos in tempPos:
                for j in range(numPoints+1):
                    self.positions.append( [pos[i] + (j) * spacing[i] for i in range(2)] )
        else:
            geometry     = args[0]
            initialPoint = args[1]
            numPoints    = args[2]
            spacing      = args[3]
            super().__init__(geometry, initialPoint)
            self.positions = [[initialPoint[i] + (x+1) * spacing[i] for i in range(2)] for x in range(numPoints)]

class IrregularLinearPattern(Pattern):
    def __init__(self, geometry = None, initialPoint = [0,0], spacings = [[1,0]]):
        super().__init__(geometry, initialPoint)
        self.positions = [initialPoint]
        for spacing in spacings:
            self.positions.append([self.positions[-1][i]+spacing[i] for i in range(2)])
        self.positions.pop(0)