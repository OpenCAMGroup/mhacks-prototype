from __future__ import division

import math

# import opencam as oc
# import opencam.materials as mat
# import opencam.geometry as geo
# import opencam.patterns as pat

# mach = oc.Machine()
# mach.material = mat.InsulationFoam
# mach.tool = 'Carbide'

# w1 = oc.Workpiece()
# w1.height = 1.5

# mach.curWorkpiece = w1

def step_range(start, end, step):
    assert step != 0

    delta = end - start
    n_steps = math.ceil(delta / step)
    if n_steps == 0:
        yield start
        return

    step = delta / n_steps
    for t in range(n_steps+1):
        yield start + step * t

SAFE = 1
CLEAR = 0.2


def hemi_pocket(x0, y0, r):
    # Start seeking at the safe height
    print('G00 Z{:.4f}'.format(SAFE))
    # Move to the center of the pocket
    print('G00 X{:.4f} Y{:.4f}'.format(x0, y0))
    # Clearance height
    print('G01 Z{:.4f}'.format(CLEAR))
    radius_step = 1/16
    for r in step_range(0, r, radius_step):
        hemi_shell(x0, y0, r)
    # We want to be safe again
    print('G00 Z{:.4f}'.format(SAFE))


def hemi_shell(x0, y0, r):
    radius_step = 1/16
    print('; Cut shell for radius', r)
    for x in step_range(-r, r, radius_step):
        arc_r = math.sqrt(r*r - x*x)
        hemi_arc(x0 + x, y0, arc_r)


def hemi_arc(x0, y0, r):
    # Go to clearance height just for safety
    print('; Cut arc at x = {:.4f} radius {:.4f}'.format(x0, r))
    print('G00 Z{:.4f}'.format(CLEAR))
    # The correct plane
    print('G19')
    # The initial point above the top of the arc
    print('G00 X{:.4f} Y{:.4f}'.format(x0, y0 + r))
    # Touch the surface
    print('G01 Z0')
    # Cut an arc centered along the horizontal diameter of a circle, cutting
    # down to the bottom point of the circle.
    print('G02 J{:.4f} K0 Y{:.4f}'.format(-r, y0 - r))
    # Return to clearance height
    print('G00 Z{:.4f}'.format(CLEAR))

print('''
G20 G90 D200 G40; Inch units. Absolute mode. Activate tool offset. Deactivate tool nose radius compensation.
G50 S2000
G96 S854 M03
F.05
''')
hemi_pocket(0, 0, 0.5)
