from .command import Command


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


def translate_pos(pos, x=0, y=0, z=0):
    result = {}
    if 'x' in pos:
        result['x'] = pos['x'] + x
    if 'y' in pos:
        result['y'] = pos['y'] + y
    if 'z' in pos:
        result['z'] = pos['z'] + z
    return result


def rotate_pos(pos, x=0, y=0, z=0):
    assert x % 90 == 0 and y % 90 == 0 and z % 90 == 0

    x %= 360; y %= 360; z %= 360
    def negate(x):
        if x is not None:
            return -x

    pos = {k: v for k, v in pos.items()}

    if x == 90:
        pos['y'], pos['z'] = negate(pos.get('z')), pos.get('y')
    elif x == 180:
        pos['y'] = negate(pos.get('y'))
        pos['z'] = negate(pos.get('z'))
    elif x == 270:
        pos['y'], pos['z'] = pos.get('z'), negate(pos.get('y'))

    if y == 90:
        pos['x'], pos['z'] = pos.get('z'), negate(pos.get('x'))
    elif y == 180:
        pos['x'] = negate(pos.get('x'))
        pos['z'] = negate(pos.get('z'))
    elif y == 270:
        pos['x'], pos['z'] = negate(pos.get('z')), pos.get('x')

    if z == 90:
        pos['x'], pos['y'] = negate(pos.get('y')), pos.get('x')
    elif z == 180:
        pos['x'] = negate(pos.get('x'))
        pos['y'] = negate(pos.get('y'))
    elif z == 270:
        pos['x'], pos['y'] = pos.get('y'), negate(pos.get('x'))

    return {k: v for k, v in pos.items() if v is not None}


class GCode(Command):
    pass


class Raw(Command):
    def __init__(self, code):
        super().__init__(self)
        self.code = code

    def gcode(self):
        return [self.code]

    def translated(self, *args):
        return Raw(self.code)

    def rotated(self, *args):
        return Raw(self.code)


class Empty(Command):
    def __init__(self):
        super().__init__(self)

    def gcode(self):
        return []

    def translated(self, *args):
        return Empty()

    def rotated(self, *args):
        return Empty()


class Goto(Command):
    def __init__(self, pos, fast=False, feed=None):
        super().__init__(self)
        self.pos, self.fast, self.feed = normalize_position(pos), fast, feed

    def gcode(self):
        if self.fast:
            G = 'G00 '
        else:
            G = 'G01 '
        positions = []
        for key in 'xyz':
            if key in self.pos and self.pos[key] is not None:
                positions.append('{}{}'.format(key.upper(), round(self.pos[key], 4)))
        feed = ''
        if self.feed:
            feed = ' F{:.01f}'.format(self.feed)
        return [G + ' '.join(positions) + feed]

    def translated(self, x=0, y=0, z=0):
        return Goto(translate_pos(self.pos, x, y, z), self.fast, self.feed)

    def rotated(self, x=0, y=0, z=0):
        return Goto(rotate_pos(self.pos, x, y, z), self.fast, self.feed)


class Spindle(Command):
    def __init__(self, turn=None):
        super().__init__(self)
        self.turn = turn

    def gcode(self):
        if self.turn is None:
            return ['M5']
        return ['S{} M3'.format(self.turn)]

    def translated(self, *args):
        return Spindle(self.turn)

    def rotated(self, *args):
        return Spindle(self.turn)



class Comment(Command):
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def gcode(self):
        return ['({})'.format(self.message)]

    def translated(self, *args):
        return Comment(self.message)

    def rotated(self, *args):
        # Joke: Should turn (Comment) into:
        # (C)
        # (o)
        # (m) ...
        return Comment(self.message)


class Arc(Command):
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
            if key in end and end[key] is not None:
                ends.append('{}{}'.format(key.upper(), round(end[key], 4)))
        center = normalize_position(self.center)
        centers = []
        for key, name in zip('xyz', 'IJK'):
            if key in center and center[key] is not None:
                centers.append('{}{}'.format(name, round(center[key], 4)))
        gcode.append('{} {} {}'.format(G, ' '.join(centers), ' '.join(ends)))

        return gcode

    def translated(self, x=0, y=0, z=0):
        return Arc(translate_pos(self.start, x, y, z),
                  self.center,
                   translate_pos(self.end, x, y, z),
                   plane=self.plane,
                   clockwise=self.clockwise)

    def rotated(self, x=0, y=0, z=0):
        assert x % 90 == 0 and y % 90 == 0 and z % 90 == 0
        plane, counter = SetPlane.rotate_plane(self.plane, x, y, z)
        clockwise = self.clockwise
        if counter < 0:
            clockwise = not self.clockwise
        return Arc(rotate_pos(self.start, x, y, z),
                   rotate_pos(self.center, x, y, z),
                   rotate_pos(self.end, x, y, z),
                   plane=plane, clockwise=clockwise)


class SetPlane(Command):
    Gs = {XY_PLANE: 'G17', XZ_PLANE: 'G18', YZ_PLANE: 'G19'}
    plane_normals = {XY_PLANE: (0, 0, 1), XZ_PLANE: (0, -1, 0), YZ_PLANE: (-1, 0, 0)}

    def __init__(self, plane=XY_PLANE):
        super().__init__(self)
        self.plane = plane

    def gcode(self):
        return [SetPlane.Gs[self.plane]]

    def translated(self, *args):
        return SetPlane(self.plane)

    def rotate_plane(plane, x=0, y=0, z=0):
        assert x % 90 == 0 and y % 90 == 0 and z % 90 == 0
        def dot(a, b):
            x0, y0, z0 = a
            x1, y1, z1 = b['x'], b['y'], b['z']
            return x0*x1 + y0*y1 + z0*z1

        point = normalize_position(SetPlane.plane_normals[plane])
        point = rotate_pos(point, x, y, z)
        for plane, normal in SetPlane.plane_normals.items():
            the_dot = dot(normal, point)
            if the_dot > 0.99:
                return plane, 1
            elif the_dot < -0.99:
                return plane, -1
        return None

    def rotated(self, x=0, y=0, z=0):
        assert x % 90 == 0 and y % 90 == 0 and z % 90 == 0
        plane, _ = SetPlane.rotate_plane(self.plane, x, y, z)
        return SetPlane(plane)
