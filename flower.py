import opencam
import opencam.gcode as gcode
import hemisphere
import ellipsoid
import actions
import math

CLEAR = 0.2
SAFE = 1.0


def flower(inner_r, outer_r, depth, n):
    mid_r = (inner_r + outer_r) / 2
    middle_space = mid_r * math.pi
    middle_axis = middle_space / (n * 1.5)
    result = gcode.Comment("A BEAUTIFUL FLOWER")
    for r in range(n):
        angle = r / n * math.pi * 2
        center = mid_r * math.cos(angle), mid_r * math.sin(angle)
        outer = outer_r * math.cos(angle), outer_r * math.sin(angle)
        result += ellipsoid.pocket(center, outer, middle_axis, depth)
    return result


data = gcode.Raw('''\
(T1 D=0.125 CR=0.015 - ZMIN=-1. - BULLNOSE END MILL)
G90 G94 G17
G20
T1 M6
G54
S8000 M3
''')

N_SIDES = 9
data += gcode.Goto({'z': SAFE}, fast=True, feed=70)
data += hemisphere.hemi_pocket(0.4)
data += flower(inner_r=0.6, outer_r=1.5, depth=0.2, n=N_SIDES)
data += actions.at_points(
    actions.drill_hole(1),
    actions.regular_polygon(N_SIDES, r=1))

data += gcode.Raw('''
G28
M30''')

opencam.print_blocks(data)
