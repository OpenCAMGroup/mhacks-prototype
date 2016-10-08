import operator

class Pattern:
    def __init__(self, geometry = None, initialPoint = [0,0]):
        self.initialPoint = initialPoint
        self.positions = []
        self.geometry = geometry

class RegularLinearPattern(Pattern):
    # sometimes I wish python had function overloading
    # true inputs: numPoints, e.g. 5
    #              spacing, e.g. [1,2]
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
            self.positions.pop(0)
        else:
            geometry     = args[0]
            initialPoint = args[1]
            numPoints    = args[2]
            spacing      = args[3]
            super().__init__(geometry, initialPoint)
            self.positions = [[initialPoint[i] + (x+1) * spacing[i] for i in range(2)] for x in range(numPoints)]

class IrregularLinearPattern(Pattern):
    def toCumulative(self, spacings):
        retList = []
        for i in range(len(spacings)):
            retList.append([sum([x[j] for x in spacings[:i+1]]) for j in range(2)])
        return retList

    # true inputs: spacings, e.g. [ [1,2], [0,1], [3,2] ]
    def __init__(self, *args):
        if isinstance(args[0], Pattern):
            pattern      = args[0]
            geometry     = pattern.geometry
            initialPoint = pattern.initialPoint
            spacings     = args[1]
            super().__init__(geometry, initialPoint)
            
            cumuSpacings = [[0,0]]
            cumuSpacings.extend(self.toCumulative(spacings))
            tempPos = [initialPoint]
            tempPos.extend(pattern.positions)
            for pos in tempPos:
                for spacing in cumuSpacings:
                    self.positions.append([pos[i] + spacing[i] for i in range(2)])
            self.positions.pop(0)
        else:
            geometry     = args[0]
            initialPoint = args[1]
            spacings     = args[2]
            super().__init__(geometry, initialPoint)

            cumuSpacings = self.toCumulative(spacings)
            for spacing in cumuSpacings:
                self.positions.append([initialPoint[i] + spacing[i] for i in range(2)])