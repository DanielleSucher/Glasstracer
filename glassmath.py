# helpful references:
# https://github.com/thomasballinger/raycasting/blob/master/vectormath.py
# http://stackoverflow.com/questions/4938332/line-plane-intersection-based-on-points

import numpy


def get_line_intersection_with_plane(line, points):
    # takes a vector (tuple of 2 points, each with a tuple of 3 coordinates)
    # and a tuple of three points of a plane (starting, end x, end y)
    lp1, lp2 = numpy.array(line)
    lv = lp2 - lp1
    p1, p2, p3 = numpy.array(points)

    normal_vector = numpy.cross(p2 - p1, p3 - p1)

    t = numpy.dot(normal_vector,
        p1 - lp1) / numpy.dot(normal_vector, lv)
    p = lp1 + lv * t
    return p
