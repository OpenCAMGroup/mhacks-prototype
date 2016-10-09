class CommandIterator(object):
    def __init__(self, obj):
        self.obj = obj

    def __next__(self):
        obj = self.obj
        if obj is None:
            raise StopIteration
        self.obj = next(self.obj)
        return obj


class Command(object):
    def __init__(self, a, b=None):
        self.a, self.b = a, b

    def __add__(self, other):
        return Command(self, other)

    def __iter__(self):
        return CommandIterator(self)

    def __next__(self):
        return self.b

    def gcode(self):
        if self.b is None:
            return self.a.gcode()
        return self.a.gcode() + self.b.gcode()

    def translated(self, x=0, y=0, z=0):
        a = self.a.translated(x, y, z)
        b = None
        if self.b is not None:
            b = self.b.translated(x, y, z)
        return Command(a, b)

    def rotated(self, x=0, y=0, z=0):
        # This isn't ideal, but is necessary night now
        assert x % 90 == 0 and y % 90 == 0 and z % 90 == 0
        a = self.a.rotated(x, y, z)
        b = None
        if self.b is not None:
            b = self.b.rotated(x, y, z)
        return Command(a, b)
