import pickle
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from copy import deepcopy

with open("bigjohn.pkl", "rb") as f:
    font = pickle.load(f)

def bounds(letter):
    points = []
    for i in letter[0]:
        points += i
    xs = [x[0] for x in points]
    max_x = max(xs)
    min_x = min(xs)
    ys = [x[1] for x in points]
    max_y = max(ys)
    min_y = min(ys)
    return (max_x - min_x, max_y - min_y)


def scale(x, s):
    x[1] *= s
    x[0] *= s
    return x

def lower_bound(curves):
    points = []
    for curve in curves:
        points += curve
    ys = [x[1] for x in points]
    return min(ys)

def translate(x, delta):
    x[0] += delta
    return x

def scale_letter(letter, bound):
    if len(letter[0]) == 0:
        return (letter[0], letter[1]* bound, letter[1]*bound)
    off = letter[1] * bound
    for i, j in enumerate(letter[0]):
        for k, point in enumerate(j):
            letter[0][i][k] = scale(letter[0][i][k], bound)
    return (letter[0], off, bounds(letter)[0])

def translate_letter(letter, delta):
    if len(letter[0]) == 0:
         return (letter[0], letter[1], letter[1])
    off = letter[1] 
    for i, j in enumerate(letter[0]):
        for k, point in enumerate(j):
            letter[0][i][k] = translate(letter[0][i][k], delta)
    return (letter[0], off, bounds(letter)[0])

def translate_word_up(curves, delta):
    for x in curves:
        for p in x:
            p[1] = p[1] + delta
    return curves

unit = bounds(font["M"])[0]

for i in font.keys():
    font[i] = scale_letter(font[i], 1/unit)
font[' '] = ([], 1, 0)

def translate_string(st, max_width):
    curves = []
    letters = []
    width = 0
    for i,j in enumerate(st):
       letter = font[j]
       width += letter[2]
       if i != 0:
           width += letter[1] * .5
    scale_factor = max_width/width
    width = 0
    letters = []
    previous = 0
    for i, j in enumerate(st):
        letter = deepcopy(font[j])
        letter = scale_letter(letter, scale_factor)
        if i != 0:
            letter = translate_letter(letter, letter[1]* .25)
        letter = translate_letter(letter, width)

        if i != 0:
            width += letter[1] * .25
        width += letter[2]

        letters.append(letter)
    for letter in letters:
        curves += letter[0]
        
    curves = translate_word_up(curves, -1 * lower_bound(curves))
    with open("svg.pkl" , "wb") as f:
        pickle.dump(curves, f)
    return curves
# curves =  translate_string("Hello world!", 7)
# curves = translate_string("riesling aa",1)

'''
fig = plt.figure()
ax = fig.add_subplot(111)
for verts in curves:

    codes = [Path.MOVETO] + [Path.LINETO for x in verts][1:]# + [Path.CLOSEPOLY]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', lw=2)
    ax.add_patch(patch)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
#plt.show()
'''



