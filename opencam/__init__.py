from .materials import InsulationFoam

class Machine:
    def __init__(self):
        self.curWorkpiece = None
        self.material = None # example: InsulationFoam
        self.tool = None # example: 'Carbide'
        self.overriddenSFM = None

    def getSFM(self):
        if self.overriddenSFM == None:
            return self.material.SFM[self.tool]
        else:
           return self.overriddenSFM

    def setSFM(self, val = None):
        self.overriddenSFM = val

    def submit(self,  workpiece):
        return


class Workpiece:
    def __init__(self):
        self.height = None # example: 0
        self.origin = None # example: [0,0]
        self.maxSize = None # example: [5,6]
