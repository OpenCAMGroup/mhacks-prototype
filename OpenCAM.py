from Materials import InsulationFoam

class Machine:
    def __init__(self):
        self.workpiece = None
        self.material = InsulationFoam
        self.tool = 'Carbide'
        self.overriddenSFM = None

    def getSFM(self):
        if self.overriddenSFM == None:
            return self.material.SFM[self.tool]
        else:
           return self.overriddenSFM

    def setSFM(self, val = None):
        self.overriddenSFM = val

class Workpiece:
    def __init__(self):
        self.height = None # example: 0
        self.origin = None # example: [0,0]
        self.maxSize = None # example: [5,6]