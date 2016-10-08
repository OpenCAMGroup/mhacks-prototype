import OpenCAM as oc
import Materials as mat
import Geometry as geo
import Patterns as pat

mach = oc.Machine()
mach.material = mat.InsulationFoam
mach.tool = 'Carbide'

w1 = oc.Workpiece()
w1.height = 1.5

mach.curWorkpiece = w1

c1 = geo.Circle(radius = 1)
pat1 = pat.RegularLinearPattern(c1, [0,0], 3, [1,0])
pat2 = pat.IrregularLinearPattern(c1, [0,0], [[1,1], [2,1], [3,1]])
pat3 = pat.RegularLinearPattern(pat1, 3, [0,1])
pat4 = pat.IrregularLinearPattern(pat1, [[0,1], [1,1], [2,2]])

geo.printStart()
d = geo.Drill(1.5)
d.printDrills(pat.RectHolePattern([0,0], [6,6]), 0.5)