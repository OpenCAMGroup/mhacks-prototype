from svg.path import parse_path
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import filterline
import rdp
from lxml import etree
import pickle
from copy import deepcopy


def process_font(filename, epsilon):
    with open(filename, "r") as f:
        contents = f.read()
    root = etree.fromstring(contents)
    glyphs = root.xpath('//*[local-name() = "glyph"]')
    finished_verts = {}
    for glyph in glyphs:
        name = glyph.xpath(".//@unicode")
        name = unicode(name[0]) if len(name) > 0 else ""
        d = glyph.xpath(".//@d")
        adv = glyph.xpath(".//@horiz-adv-x")
        adv = adv[0] if len(adv) > 0 else 0
        if len(d) != 0:
            d = d[0]
            finished_verts[unicode(name)] = (list(process_glyph(d, epsilon)), int(adv))
        else:
            finished_verts[unicode(name)] = ([], int(adv))
        print name + " done"
    return finished_verts



def process_glyph(d, epsilon):
    paths2 = d[1:-1].split("M")
    paths2 = [x.rstrip() for x in paths2]
    paths = []
    for i in paths2:
        if i[0] != "M":
            path = "M" + i
            if i[-1] != "z":
                path += "z"
            paths.append(path)
    samples = 2000

    paths = map(parse_path, paths)


    #fig = plt.figure()
    vert_array = []
    for path in paths:
        points = []
        for i in range(samples):
            points.append(path.point(1.0/samples * i))

        verts = [(z.real, z.imag) for z in points]
        verts.append(verts[0])
        verts = rdp.rdp(verts, epsilon=epsilon)
        vert_array.append(verts)
        codes = [Path.MOVETO] + [Path.LINETO for x in verts][1:]# + [Path.CLOSEPOLY]


        path = Path(verts, codes)


        #ax = fig.add_subplot(111)
        #patch = patches.PathPatch(path, facecolor='none', lw=2)
        #ax.add_patch(patch)
        #ax.set_xlim(-300,1000)
        #ax.set_ylim(-300,1000)
    #plt.show()
    return vert_array

zapfino = process_font("riesling.svg", 1)

with open("riesling.pkl", "w") as f:
    pickle.dump(zapfino, f)


