import pickle
import geometry as geo
import gcode

def print_blocks(blocks):
    for block in blocks:
        print('\n'.join(block.gcode()))

with open('svg.pkl', 'rb') as pickle_file:
    content = pickle.load(pickle_file)


blocks = ( gcode.Spindle(True) )

for curve in content:
    a = geo.Polygon(curve, 0.2)
    blocks += a.printPolygon((0,1))

blocks += ( gcode.Spindle(False) )


print_blocks(blocks)