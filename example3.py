import pickle
import geometry as geo

def print_blocks(blocks):
    for block in blocks:
        print('\n'.join(block.gcode()))

with open('svg.pkl', 'rb') as pickle_file:
    content = pickle.load(pickle_file)

for curve in content:
    a = geo.Polygon(curve, 0.2)
    blocks = a.printPolygon()
    print_blocks(blocks)