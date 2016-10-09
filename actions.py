import opencam.gcode as gcode
import math

CLEAR = 0.2
SAFE = 1.0


def inch(x):
    return x


def mm(x):
    return inch(x) / 25.4


def bore_cylinder(r, depth, tool_diameter=inch(1/8), step=1/16):
    result = (gcode.Comment('Bore a cylinder hole r={}'.format(r))
              + gcode.Goto({'z': SAFE}, fast=True)
              + gcode.Goto((0, 0), fast=True)
              + gcode.Goto({'z': CLEAR}, fast=True))
    outer_radius = r - tool_diameter/2
    depth_steps = math.ceil(depth / step)
    radius_steps = math.ceil(outer_radius / step)
    for i in range(1, depth_steps + 1):
        t = i / depth_steps
        result += gcode.Goto({'z': -t * depth})
        for j in range(1, radius_steps+1):
            radius = outer_radius * j / radius_steps
            result += gcode.Arc(start=(radius, 0), center=(-radius, 0),
                            end={}, clockwise=False)
    return result


def drill_hole(depth):
    return (gcode.Comment("Drill hole depth={}".format(depth))
            + gcode.Goto({'z': SAFE}, fast=True)
            + gcode.Goto((0, 0), fast=True)
            + gcode.Goto({'z': CLEAR}, fast=True)
            + gcode.Goto({'z': -depth})
            + gcode.Goto({'z': CLEAR})
            + gcode.Goto({'z': SAFE}, fast=True))


def profile_cut(corner0, corner1, depth, step=inch(1/4), tool_diameter=inch(1/8)):
    x0 = corner0[0] - tool_diameter/2
    x1 = corner1[0] + tool_diameter/2
    y0 = corner0[1] - tool_diameter/2
    y1 = corner1[1] + tool_diameter/2
    result = (gcode.Comment("Profile cut from {0[0]}x{0[1]} to {1[0]}x{1[1]}"
                          .format(corner0, corner1))
            + gcode.Goto({'z': SAFE}, fast=True)
            + gcode.Goto((x0, y0), fast=True)
            + gcode.Goto({'z': CLEAR}, fast=True))
    n_steps = math.ceil(depth / step)
    for i in range(1, n_steps + 1):
        t = i / n_steps
        result += (gcode.Goto({'z': -depth * t})
                   + gcode.Goto((x0, y0))
                   + gcode.Goto((x0, y1))
                   + gcode.Goto((x1, y1))
                   + gcode.Goto((x1, y0))
                   + gcode.Goto((x0, y0)))
    return result

def at_points(geom, points):
    result = gcode.Empty()
    for x, y in points:
        result += geom.translated(x=x, y=y)
    return result

