from __future__ import division

import math

import opencam.gcode as gcode


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
    result = (gcode.Goto({'z': SAFE}, fast=True) +
              gcode.Goto((x0, y0), fast=True) +
              gcode.Goto({'z': CLEAR}))

    radius_step = 1/16
    for r0 in step_range(0, r - radius_step, radius_step):
        result += hemi_shell(x0, y0, r0, radius_step)
    # Do the fine grained smoothing step along both axes
    result += hemi_shell(x0, y0, r, radius_step/2)
    result += hemi_shelly(x0, y0, r, radius_step/2)
    # We want to be safe again
    return result + gcode.Goto({'z': SAFE})


def hemi_shell(x0, y0, r, radius_step=1/16):
    result = gcode.Comment('Cut shell for radius ' + str(r))
    for x in step_range(-r, r, radius_step):
        arc_r = math.sqrt(r*r - x*x)
        result += hemi_arc(x0 + x, y0, arc_r)
    return result


def hemi_shelly(x0, y0, r, radius_step=1/16):
    result = gcode.Comment('Cut shell for radius ' + str(r))
    for y in step_range(-r, r, radius_step):
        arc_r = math.sqrt(r*r - y*y)
        result += hemi_arcy(x0, y0 + y, arc_r)
    return result

def hemi_arc(x0, y0, r):
    # Go to clearance height just for safety
    return (gcode.Comment('Cut arc at x = {:.4f} radius {:.4f}'.format(x0, r))
            + gcode.Goto({'z': CLEAR}, fast=True)
            + gcode.Goto((x0, y0 + r), fast=True)
            + gcode.Arc(start={'z': 0}, end={'y': y0 - r},
                        center={'y': -r, 'z': 0}, plane='yz')
            + gcode.Goto({'z': CLEAR}))


def hemi_arcy(x0, y0, r):
    # Go to clearance height just for safety
    return (gcode.Comment('Cut arc at x = {:.4f} radius {:.4f}'.format(x0, r))
            + gcode.Goto({'z': CLEAR}, fast=True)
            + gcode.Goto((x0 - r, y0), fast=True)
            + gcode.Arc(start={'z': 0}, end={'x': x0 + r},
                        center={'x': r, 'z': 0}, plane='xz')
            + gcode.Goto({'z': CLEAR}, fast=True))


def print_blocks(blocks):
    for block in blocks:
        print('\n'.join(block.gcode()))


print('''
G20 G90 ; Inch units. Absolute mode.
D200 G40 ; Activate tool offset. Deactivate tool nose radius compensation.
G94 S2000 M03 F8
''')
print_blocks(hemi_pocket(0, 0, 0.5))
