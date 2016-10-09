from opencam import gcode

import math

CLEAR = 0.2
SAFE = 1.0


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


def hemi_pocket(r, radius_step=1/16):
    result = (gcode.Goto({'z': SAFE}, fast=True, feed=70) +
              gcode.Goto((0, 0), fast=True) +
              gcode.Goto({'z': CLEAR}))

    radius_step = 1/16
    for r0 in step_range(0, r - radius_step, radius_step):
        result += hemi_shell(r0, radius_step)
    # Do the fine grained smoothing step along both axes
    surfacing_shell = hemi_shell(r, radius_step/2)
    result += surfacing_shell
    result += surfacing_shell.rotated(z=90)
    # We want to be safe again
    return result + gcode.Goto({'z': SAFE})


def hemi_shell(r, radius_step=1/16):
    result = gcode.Comment('Cut shell for radius ' + str(r))
    for x in step_range(r, -r, radius_step):
        arc_r = math.sqrt(r*r - x*x)
        # Cutting zero-radius arcs are silly
        if arc_r < 0.01:
            continue
        result += hemi_arc(arc_r).translated(x=x)
    return result


def hemi_arc(r):
    # Go to clearance height just for safety
    return (gcode.Comment('Cut arc radius {:.4f}'.format(r))
            + gcode.Goto({'z': CLEAR}, fast=True)
            + gcode.Goto((0, -r), fast=True)
            + gcode.Arc(start={'z': 0}, end={'y': r},
                        center={'y': r, 'z': 0}, plane='yz',
                        clockwise=False)
            + gcode.Goto({'z': CLEAR}))
