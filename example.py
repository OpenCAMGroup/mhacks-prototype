import OpenCAM as oc
import Materials as mat

mach = oc.Machine()
mach.material = mat.InsulationFoam
mach.tool = 'Carbide'

w1 = oc.Workpiece()
w1.height = 1.5

