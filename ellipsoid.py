from __future__ import division

from opencam import gcode

import math

CLEAR = 0.2
SAFE = 1.0

def circle_interpolate(t):
    return math.sqrt(1 - t*t)


def pocket(center, major_vertex, minor_axis, depth, step=1/16):
    result = (gcode.Comment("Cut ellipsoidal pocket {0[0]} {0[1]} {1[0]} {1[1]} {2} {3} {4}"
                            .format(center, major_vertex, minor_axis, depth, step))
              + gcode.Goto({'z': SAFE}, fast=True)
              + gcode.Goto(center))

    minor_length = minor_axis
    dx, dy = major_vertex[0] - center[0], major_vertex[1] - center[1]
    major_length = math.sqrt(dx*dx + dy*dy)

    factor = minor_length/major_length
    dx0, dy0 = -dy * factor, dx * factor

    max_size = max(major_length, depth)
    n_steps = math.ceil(max_size / step) // 2
    for i in range(n_steps+1):
        t = i / n_steps
        result += ellipse_shell(center, (dx * t, dy * t),
                                (dx0 * t, dy0 * t), depth * t, step)
    result += ellipse_shell(center, (dx, dy), (dx0, dy0), depth, step/2)
    result += ellipse_shell(center, (dx0, dy0), (dx, dy), depth, step/2)
    return result


def ellipse_shell(center, major_axis, minor_axis, depth, step=1/16):
    result = gcode.Comment("Cut ellipse shell {0[0]} {0[1]} {1[0]} {1[1]} {2[0]} {2[1]} {3} {4}".format(
        center, major_axis, minor_axis, depth, step))
    max_size = max(math.sqrt(major_axis[0]**2 + major_axis[1]**2), depth)
    n_steps = math.ceil(max_size / step)
    if n_steps == 0:
        return gcode.Empty()
    for i in range(-n_steps, n_steps+1):
        t = i / n_steps
        s = circle_interpolate(t)
        cx, cy = center[0] + major_axis[0] * t, center[1] + major_axis[1] * t
        px, py = minor_axis[0] * s, minor_axis[1] * s
        result += ellipse_arc((cx, cy), (px, py), depth * s)
    return result


def ellipse_arc(center, displacement, depth, steps=32):
    result = (gcode.Comment("Cut ellipse arc {0[0]} {0[1]} {1[0]} {1[1]} {2} {3}"
                            .format(center, displacement, depth, steps))
              + gcode.Goto({'z': CLEAR}, fast=True)
              + gcode.Goto((center[0] - displacement[0], center[1] - displacement[1]),
                           fast=True))
    count = steps//2
    for i in range(-count, count+1):
        t = i/count
        x = center[0] + displacement[0] * t
        y = center[1] + displacement[1] * t
        z = -depth * circle_interpolate(t)
        result += gcode.Goto((x, y, z))
    result += gcode.Goto({'z': CLEAR})
    return result
