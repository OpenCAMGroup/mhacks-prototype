class Command(object):
    def __init__(self, *elements):
        self.members = list(elements)

    def __add__(self, other):
        if self.__class__ == Command:
            new_command = Command()
            new_command.members = self.members + [other]
            return new_command
        return Command(self, other)

    def gcode(self):
        result = []
        for member in self.members:
            if member is not None:
                result += member.gcode()
        return result

    def translated(self, x=0, y=0, z=0):
        members = [m.translated(x, y, z) for m in self.members
                   if m is not None and m is not self]
        new_command = Command()
        new_command.members = members
        return new_command

    def rotated(self, x=0, y=0, z=0):
        # This isn't ideal, but is necessary night now
        assert x % 90 == 0 and y % 90 == 0 and z % 90 == 0
        members = [m.rotated(x, y, z) for m in self.members
                   if m is not None and m is not self]
        new_command = Command()
        new_command.members = members
        return new_command
