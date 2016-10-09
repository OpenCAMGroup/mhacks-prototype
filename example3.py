from __future__ import division

import opencam.gcode as gcode
import hemisphere
import math

CLEAR = 0.2
SAFE = 1.0


def print_blocks(data):
    print('%')
    print('\n'.join(data.gcode()))
    print('%')


def regular_polygon(item, n=5, r=1):
    result = gcode.Empty()
    for i in range(n):
        angle = i / n * 2 * math.pi
        x, y = math.cos(angle) * r, math.sin(angle) * r
        result += item.translated(x, y)
    return result


def polystar(n=5, r=1, t=2):
    result = (gcode.Goto({'z': CLEAR}, fast=True)
              + gcode.Goto((r, 0), fast=True)
              + gcode.Goto({'z': -0.1}))
    for i in range(n+1):
        angle = i / n * 2 * math.pi
        x, y = math.cos(angle) * r, math.sin(angle) * r
        result += gcode.Goto((x, y))
    for i in range(n+1):
        angle = i * t / n * 2 * math.pi
        x, y = math.cos(angle) * r, math.sin(angle) * r
        result += gcode.Goto((x, y))
    return result


data = gcode.Raw('''\
(T1 D=0.125 CR=0.015 - ZMIN=-1. - BULLNOSE END MILL)
G90 G94 G17
G20
T1 M6
G54
S8000 M3
''')

N_SIDES = 7
data += hemisphere.hemi_pocket(0.5)
pocket = hemisphere.hemi_pocket(0.3)
data += regular_polygon(pocket, 7, 2)
data += polystar(7, 2)
data += gcode.Goto({'z': CLEAR})
data += gcode.Raw('''
G28
M30''')

print_blocks(data)
