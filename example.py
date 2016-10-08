from __future__ import division

import math

import opencam.gcode as gcode


def step_range(start, end, step):
    assert step != 0

    delta = end - start
    n_steps = math.ceil(abs(delta) / step)
    if n_steps == 0:
        yield start
        return

    step = delta / n_steps
    for t in range(n_steps+1):
        yield start + step * t

SAFE = 1
CLEAR = 0.2


def hemi_pocket(x0, y0, r):
    result = (gcode.Goto({'z': SAFE}, fast=True, feed=70) +
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
    for x in step_range(r, -r, radius_step):
        arc_r = math.sqrt(r*r - x*x)
        # Cutting zero-radius arcs are silly
        if arc_r < 0.01:
            continue
        result += hemi_arc(x0 + x, y0, arc_r)
    return result


def hemi_shelly(x0, y0, r, radius_step=1/16):
    result = gcode.Comment('Cut shell for radius ' + str(r))
    for y in step_range(r, -r, radius_step):
        arc_r = math.sqrt(r*r - y*y)
        # Cutting zero-radius arcs are silly
        if arc_r < 0.01:
            continue
        result += hemi_arcy(x0, y0 + y, arc_r)
    return result

def hemi_arc(x0, y0, r):
    # Go to clearance height just for safety
    return (gcode.Comment('Cut arc at x = {:.4f} radius {:.4f}'.format(x0, r))
            + gcode.Goto({'z': CLEAR}, fast=True)
            + gcode.Goto((x0, y0 - r), fast=True)
            + gcode.Arc(start={'z': 0}, end={'y': y0 + r},
                        center={'y': r, 'z': 0}, plane='yz',
                        clockwise=False)
            + gcode.Goto({'z': CLEAR}))


def hemi_arcy(x0, y0, r):
    # Go to clearance height just for safety
    return (gcode.Comment('Cut arc at x = {:.4f} radius {:.4f}'.format(x0, r))
            + gcode.Goto({'z': CLEAR}, fast=True)
            + gcode.Goto((x0 + r, y0), fast=True)
            + gcode.Arc(start={'z': 0}, end={'x': x0 - r},
                        center={'x': -r, 'z': 0}, plane='xz',
                        clockwise=False)
            + gcode.Goto({'z': CLEAR}, fast=True))


def print_blocks(blocks):
    for block in blocks:
        print('\n'.join(block.gcode()))

print('''\
%
(T1  D=0.125 CR=0.015 - ZMIN=-1. - BULLNOSE END MILL)
G90 G94 G17
G20
T1 M6
G54
S8000 M3
''')
data = hemi_pocket(0, 0, 0.5)
data += gcode.Goto({'z': CLEAR}, fast=True)
print_blocks(data)
print('''
G28
M30
% ''')
