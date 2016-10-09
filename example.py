from __future__ import division

import opencam.gcode as gcode
import hemisphere

CLEAR = 0.2
SAFE = 1.0


def print_blocks(data):
    print('%')
    print('\n'.join(data.gcode()))
    print('%')

data = gcode.Raw('''\
(T1 D=0.125 CR=0.015 - ZMIN=-1. - BULLNOSE END MILL)
G90 G94 G17
G20
T1 M6
G54
S8000 M3
''')
data += hemisphere.hemi_pocket(0.5)
data += gcode.Goto({'z': CLEAR}, fast=True)
data += gcode.Raw('''
G28
M30''')
print_blocks(data)
