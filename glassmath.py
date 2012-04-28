import numpy
import math


def get_normal(points):
    p1, p2, p3 = numpy.array(points)
    normal = numpy.cross(p2 - p1, p3 - p1)
    return normal


def get_unit_normal(points):
    normal = get_normal(points)
    return normal / numpy.linalg.norm(normal)


def get_line_intersection_with_plane(line, points, normal):
    # takes a vector (tuple of 2 points, each with a tuple of 3 coordinates)
    # and a tuple of three points of a plane (starting, end x, end y)
    lp1, lp2 = numpy.array(line)
    lv = lp2 - lp1
    p1, p2, p3 = numpy.array(points)

    t = numpy.dot(normal,
        p1 - lp1) / numpy.dot(normal, lv)

    return lp1 + lv * t


def get_vector_from_ray(ray):
    v = numpy.array(ray[1]) - numpy.array(ray[0])
    return v


def norm(vec):
    return numpy.array(vec) / numpy.sqrt(numpy.dot(numpy.array(vec), numpy.array(vec)))


def refract(ray, normal, points, n1, n2):
    point1 = get_line_intersection_with_plane(ray, (points[0], points[1], points[2]), normal)
    n = n1 / n2
    vector = get_vector_from_ray((ray[1], point1))
    dot = numpy.dot(normal, norm(vector))
    c = numpy.sqrt(numpy.absolute(1 - math.pow(n, 2) * (1 - math.pow(dot, 2))))
    vec = (n * vector) - (n * dot - c) * normal
    return point1.astype(int), norm(vec).astype(int)

# helpful references:
# https://github.com/thomasballinger/raycasting/blob/master/vectormath.py
# http://stackoverflow.com/questions/4938332/line-plane-intersection-based-on-points
