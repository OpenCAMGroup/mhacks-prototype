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
    result = (gcode_goto({'z': SAFE}, fast=True) +
              gcode_goto((x0, y0), fast=True) +
              gcode_goto({'z': CLEAR}))

    radius_step = 1/16
    for r0 in step_range(0, r - radius_step, radius_step):
        result += hemi_shell(x0, y0, r0, radius_step)
    # Do the fine grained smoothing step along both axes
    result += hemi_shell(x0, y0, r, radius_step/2)
    result += hemi_shelly(x0, y0, r, radius_step/2)
    # We want to be safe again
    return result + gcode_goto({'z': SAFE})


def hemi_shell(x0, y0, r, radius_step=1/16):
    result = gcode_comment('Cut shell for radius ' + str(r))
    for x in step_range(-r, r, radius_step):
        arc_r = math.sqrt(r*r - x*x)
        result += hemi_arc(x0 + x, y0, arc_r)
    return result


def hemi_shelly(x0, y0, r, radius_step=1/16):
    result = gcode_comment('Cut shell for radius ' + str(r))
    for y in step_range(-r, r, radius_step):
        arc_r = math.sqrt(r*r - y*y)
        result += hemi_arcy(x0, y0 + y, arc_r)
    return result

def hemi_arc(x0, y0, r):
    # Go to clearance height just for safety
    return (gcode_comment('Cut arc at x = {:.4f} radius {:.4f}'.format(x0, r))
            + gcode_goto({'z': CLEAR}, fast=True)
            + gcode_goto((x0, y0 + r), fast=True)
            + gcode_arc(start={'z': 0}, end={'y': y0 - r},
                        center={'y': -r, 'z': 0}, plane='yz')
            + gcode_goto({'z': CLEAR}))


def hemi_arcy(x0, y0, r):
    # Go to clearance height just for safety
    return (gcode_comment('Cut arc at x = {:.4f} radius {:.4f}'.format(x0, r))
            + gcode_goto({'z': CLEAR}, fast=True)
            + gcode_goto((x0 - r, y0), fast=True)
            + gcode_arc(start={'z': 0}, end={'x': x0 + r},
                        center={'x': r, 'z': 0}, plane='xz')
            + gcode_goto({'z': CLEAR}, fast=True))


def gcode_comment(string):
    return [{'type': 'comment', 'comment': string}]


def gcode_goto(point, fast=False):
    return [{'type': 'goto', 'point': point, 'fast': fast}]


def gcode_arc(start, end, center, plane='xy', clockwise=True):
    return ([{'type': 'plane', 'plane': plane}]
            + gcode_goto(start)
            + [{'type': 'arc', 'center': center, 'end': end, 'clockwise': clockwise}])

def normalize_position(pos):
    if isinstance(pos, tuple):
        if len(pos) == 2:
            x, y = pos
            return {'x': x, 'y': y}
        elif len(pos) == 3:
            x, y, z = pos
            return {'x': x, 'y': y, 'z': z}
        else:
            assert 2 <= len(pos) <= 3
    else:
        return pos


def format_block(block):
    ty = block['type']
    if ty == 'comment':
        return '; ' + block['comment']
    elif ty == 'goto':
        pos = normalize_position(block['point'])
        if block['fast']:
            G = 'G00 '
        else:
            G = 'G01 '
        positions = []
        for key in 'xyz':
            if key in pos:
                positions.append('{}{}'.format(key.upper(), round(pos[key], 4)))
        return G + ' '.join(positions)
    elif ty == 'plane':
        Gs = {'xy': 'G17', 'xz': 'G18', 'yz': 'G19'}
        return Gs[block['plane']]
    elif ty == 'arc':
        if block['clockwise']:
            G = 'G02'
        else:
            G = 'G03'
        end = normalize_position(block['end'])
        ends = []
        for key in 'xyz':
            if key in end:
                ends.append('{}{}'.format(key.upper(), round(end[key], 4)))
        center = normalize_position(block['center'])
        centers = []
        for key, name in zip('xyz', 'IJK'):
            if key in center:
                centers.append('{}{}'.format(name, round(center[key], 4)))
        return '{} {} {}'.format(G, ' '.join(centers), ' '.join(ends))
    else:
        print('Unexpected block', block)
        assert False


def print_blocks(blocks):
    for block in blocks:
        print(format_block(block))


print('''
G20 G90 ; Inch units. Absolute mode.
D200 G40 ; Activate tool offset. Deactivate tool nose radius compensation.
G94 S2000 M03 F8
''')
print_blocks(hemi_pocket(0, 0, 0.5))
