class Pattern:
    def __init__(self, geometry = None, initialPoint = [0,0]):
        self.initialPoint = initialPoint
        self.positions = [initialPoint]
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
            self.positions = []

            for pos in pattern.positions:
                for j in range(numPoints+1):
                    self.positions.append( [pos[i] + (j) * spacing[i] for i in range(2)] )
        else:
            geometry     = args[0]
            initialPoint = args[1]
            numPoints    = args[2]
            spacing      = args[3]
            super().__init__(geometry, initialPoint)
            self.positions = [[initialPoint[i] + (x) * spacing[i] for i in range(2)] for x in range(numPoints+1)]

class IrregularLinearPattern(Pattern):
    def toCumulative(self, spacings):
        # turns a list of relative spacings into a list of cumulative spacings
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
            self.positions = []
            
            cumuSpacings = [[0,0]]
            cumuSpacings.extend(self.toCumulative(spacings))
            for pos in pattern.positions:
                for spacing in cumuSpacings:
                    self.positions.append([pos[i] + spacing[i] for i in range(2)])
        else:
            geometry     = args[0]
            initialPoint = args[1]
            spacings     = args[2]
            super().__init__(geometry, initialPoint)

            cumuSpacings = self.toCumulative(spacings)
            for spacing in cumuSpacings:
                self.positions.append([initialPoint[i] + spacing[i] for i in range(2)])