from __future__ import division

import opencam as oc

import geometry as geo
import patterns as pat


def print_blocks(blocks):
    for block in blocks:
        print('\n'.join(block.gcode()))

d = geo.Drill(1.5)
blocks = d.printDrills(pat.RectHolePattern([0,0], [6,6]))
print_blocks(blocks)
