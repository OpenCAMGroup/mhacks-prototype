XY_PLANE = 'xy'
XZ_PLANE = 'xz'
YZ_PLANE = 'yz'


def normalize_position(pos):
    if isinstance(pos, tuple):
        if len(pos) == 2:
            x, y = pos
            return {'x': x, 'y': y}
        elif len(pos) == 3:
            x, y, z = pos
            return {'x': x, 'y': y, 'z': z}
        else:
            assert 2 <= len(pos) <= 3
    else:
        return pos


class GCodeIterator(object):
    def __init__(self, obj):
        self.obj = obj

    def __next__(self):
        obj = self.obj
        if obj is None:
            raise StopIteration
        self.obj = next(self.obj)
        return obj


class GCode(object):
    def __init__(self, a, b=None):
        self.a, self.b = a, b

    def __add__(self, other):
        return GCode(self, other)

    def __iter__(self):
        return GCodeIterator(self)

    def __next__(self):
        return self.b

    def gcode(self):
        return self.a.gcode() + self.b.gcode()


class Goto(GCode):
    def __init__(self, pos, fast=False):
        super().__init__(self)
        self.pos, self.fast = pos, fast

    def gcode(self):
        pos = normalize_position(self.pos)
        if self.fast:
            G = 'G00 '
        else:
            G = 'G01 '
        positions = []
        for key in 'xyz':
            if key in pos:
                positions.append('{}{}'.format(key.upper(), round(pos[key], 4)))
        return [G + ' '.join(positions)]


class Comment(GCode):
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def gcode(self):
        return ['; ' + self.message]


class Arc(GCode):
    def __init__(self, start, center, end, plane=XY_PLANE, clockwise=True):
        super().__init__(self)
        self.start, self.center, self.end = start, center, end
        self.plane, self.clockwise = plane, clockwise

    def gcode(self):
        gcode = (SetPlane(self.plane)
                 + Goto(self.start)).gcode()
        if self.clockwise:
            G = 'G02'
        else:
            G = 'G03'
        end = normalize_position(self.end)
        ends = []
        for key in 'xyz':
            if key in end:
                ends.append('{}{}'.format(key.upper(), round(end[key], 4)))
        center = normalize_position(self.center)
        centers = []
        for key, name in zip('xyz', 'IJK'):
            if key in center:
                centers.append('{}{}'.format(name, round(center[key], 4)))
        gcode.append('{} {} {}'.format(G, ' '.join(centers), ' '.join(ends)))
        return gcode


class SetPlane(GCode):
    Gs = {XY_PLANE: 'G17', XZ_PLANE: 'G18', YZ_PLANE: 'G19'}

    def __init__(self, plane=XY_PLANE):
        super().__init__(self)
        self.plane = plane

    def gcode(self):
        return [SetPlane.Gs[self.plane]]
