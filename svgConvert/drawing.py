import rdp
from lxml import etree
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import pickle
from svg.path import parse_path







def process_path(d, epsilon):
    paths2 = d[1:-1].split("M")
    paths2 = [x.rstrip() for x in paths2]
    paths3 = []
    for i in paths2:
        split = i.split("m")
        if len(split) > 1:
            paths3.append("M" + split.pop(0))
            for j in i.split('m'):
                paths3.append("m" + j)
        else:
            paths3.append("M" + i)
    
    samples = 2000

    paths = map(parse_path, paths3)

    vert_array = []
    for path in paths:
        points = []
        for i in range(samples):
            points.append(path.point(1.0/samples * i))

        verts = [(z.real, z.imag) for z in points]
        verts.append(verts[0])
        verts = rdp.rdp(verts, epsilon=epsilon)
        vert_array.append(verts)

    return vert_array

def get_paths(filehandle, epsilon):
    with open(filehandle, "r") as f:
        contents = f.read()
    root= etree.fromstring(contents)
    paths = root.xpath('//*[local-name() = "path"]')
    geometry = []
    for i in paths:
        d = str(i.xpath(".//@d")[0])
        geometry.append(process_path(d, epsilon))
    return geometry

def get_bounds(geometry):
    points = []
    for i in geometry:
        points += i
    xs = [x[0] for x in points]
    xmin = min(xs)
    xmax = max(xs)
    ys = [x[1] for x in points]
    ymin = min(ys)
    ymax = max(ys)
    return (xmax-xmin, ymax-ymin)

def scale_points(geometry, s):
    for i, curve in enumerate(geometry):
        for j, point in enumerate(curve):
            geometry[i][j] = scale_point(point, s)
    return geometry


def scale_point(point, s):
    return [point[0] * s, point[1] * s]

geometry = get_paths("DUCKS.svg", 1)[0]
geometry = scale_points(geometry, 1.0/get_bounds(geometry)[0])
fig = plt.figure()
print geometry
for verts in geometry:

    codes = [Path.MOVETO] + [Path.LINETO for x in verts][1:]# + [Path.CLOSEPOLY]


    path = Path(verts, codes)


    ax = fig.add_subplot(111)
    patch = patches.PathPatch(path, facecolor='none', lw=2)
    ax.add_patch(patch)
    ax.set_xlim(-3,10)
    ax.set_ylim(-3,10)
plt.show()
