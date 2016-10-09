import pickle
import geometry as geo
import gcode
from translate import translate_string

def print_blocks(blocks):
    for block in blocks:
        print('\n'.join(block.gcode()))

content = translate_string("openCAM", 3.5)
content2 = translate_string("#DitchGCode", 3.5)

blocks = ( gcode.Spindle(True) )

for curve in content:
    a = geo.Polygon(curve, 0.2)
    blocks += a.printPolygon((1.25,0.75))

blocks += ( gcode.Spindle(False) )

blocks += ( gcode.Spindle(True) )

for curve in content2:
    a = geo.Polygon(curve, 0.2)
    blocks += a.printPolygon((1.25,0.25))

blocks += ( gcode.Spindle(False) )

print_blocks(blocks)