import opencam
import opencam.gcode as gcode
import actions
import hemisphere
import math

CLEAR = 0.2
SAFE = 1.0


def inch(x):
    return x


def mm(x):
    return inch(x) / 25.4


data = gcode.Raw('''\
(T1 D=0.125 CR=0.015 - ZMIN=-1. - BULLNOSE END MILL)
G90 G94 G17
G20
T1 M6
G54
S8000 M3
''')

drill_points = [(mm(20), mm(20)),
                (mm(160), mm(20)),
                (mm(160), mm(100)),
                (mm(20), mm(100))]
cylinder = actions.bore_cylinder(r=mm(5), depth=mm(5), tool_diameter=inch(1/8))
hole = actions.drill_hole(depth=inch(1))

data += gcode.Goto({'z': SAFE}, fast=True, feed=70)
data += hemisphere.hemi_pocket(mm(20)).translated(x=mm(90), y=mm(60))
data += actions.at_points(cylinder + hole, drill_points)
data += actions.profile_cut((mm(0), mm(0)), (mm(180), mm(120)),
                            depth=inch(1), tool_diameter=inch(1/8))

data += gcode.Raw('''
G28
M30''')

opencam.print_blocks(data)
