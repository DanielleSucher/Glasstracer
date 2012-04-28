# helpful references:
# https://github.com/thomasballinger/raycasting/blob/master/vectormath.py
# http://stackoverflow.com/questions/4938332/line-plane-intersection-based-on-points

import numpy
import math


def get_normal(p1, p2, p3):
    return numpy.cross(p2 - p1, p3 - p1)


def get_line_intersection_with_plane(line, points):
    # takes a vector (tuple of 2 points, each with a tuple of 3 coordinates)
    # and a tuple of three points of a plane (starting, end x, end y)
    lp1, lp2 = numpy.array(line)
    lv = lp2 - lp1

    p1, p2, p3 = numpy.array(points)

    normal_vector = get_normal(p1, p2, p3)
    # print "points: ", points
    # print normal_vector

    t = numpy.dot(normal_vector,
        p1 - lp1) / numpy.dot(normal_vector, lv)
    p = lp1 + lv * t
    return p


def get_vector_from_ray(ray):
    v = numpy.array(ray[1]) - numpy.array(ray[0])
    return v


def norm(vec):
    return numpy.array(vec) / numpy.sqrt(numpy.dot(numpy.array(vec), numpy.array(vec)))


def refract(ray, normal, points, n1, n2):
    # ray is a tuple of tuples
    point1 = get_line_intersection_with_plane(ray, (points[0], points[1], points[2]))
    n = n1 / n2
    vector = get_vector_from_ray((ray[1], point1))
    dot = numpy.dot(norm(normal), norm(vector))
    c = numpy.sqrt(1 - math.pow(n, 2) * (1 - math.pow(dot, 2)))
    vec = ((n * vector) + numpy.absolute((n * dot - c) * normal))
    return point1.astype(int), norm(vec).astype(int)
