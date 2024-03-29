import sys
import numpy
import glassmath
from PIL import Image


class Glass(object):
    """A slab of glass through which to see images"""
    def __init__(self, img, thickness, zcoord):
        self.first_z = zcoord / 2
        self.second_z = self.first_z + thickness
        self.first_points = numpy.array(((0, 0, self.first_z),
            (img.width, 0, self.first_z), (0, img.height, self.first_z)))
        # self.first_normal = glassmath.get_unit_normal(self.first_points[0], self.first_points[1], self.first_points[2])
        self.first_normal = glassmath.get_unit_normal(self.first_points)
        self.second_points = numpy.array(((0, 0, self.second_z),
            (img.width, 0, self.second_z), (0, img.height, self.second_z)))
        # self.second_normal = glassmath.get_unit_normal(self.second_points[0], self.second_points[1], self.second_points[2])
        self.second_normal = glassmath.get_unit_normal(self.second_points)


class Img(object):
    def __init__(self, imgname, zcoord):
        self.pic = Image.open(imgname)
        self.size = self.pic.size
        self.width = self.size[0]
        self.height = self.size[1]
        self.points = ((0, 0, zcoord), (self.width, 0, zcoord),
            (0, self.height, zcoord))
        self.pixels = self.pic.load()
        self.pixlist = list(self.pic.getdata())
        self.normal = glassmath.get_normal(self.points)


class ViewAndCamera(object):
    def __init__(self, img, distance):
        self.img = img
        # The view is 1/4 the size of the img, and centered
        self.width = img.width / 2
        self.height = img.height / 2
        self.x_offset = self.width / 2
        self.y_offset = self.height / 2
        self.topleftpt = (self.x_offset, self.y_offset, 0)
        self.screen_width_ray = numpy.array((self.topleftpt,
            (self.width + self.x_offset, self.y_offset,
                0)), dtype=float)
        self.screen_height_ray = numpy.array((self.topleftpt,
            (self.x_offset, self.height + self.y_offset,
                0)), dtype=float)
        self.camera_distance = distance
        # really just the center of the 2d plain,
        # with a z-coord of camera_distance
        self.camera_position = (self.width,
            self.height, self.camera_distance)

    def get_initial_rays(self):
        """sets up rays from the camera to each pixel in the grid/screen"""
        for x in xrange(self.x_offset, self.width + self.x_offset):
            for y in xrange(self.y_offset, self.height + self.y_offset):
                point = (x, y, 0)
                yield (self.camera_position, point)


class World(object):
    def __init__(self, imgname, zcoord=10, viewdistance=-4, thickness=2):
        self.img = Img(imgname, zcoord)
        self.view = ViewAndCamera(self.img, viewdistance)
        self.glass = Glass(self.img, thickness, zcoord)

    def render_image(self, filename):
        # using the high val for impure flint glass from http://en.wikipedia.org/wiki/List_of_refractive_indices
        refr_indexes = {"air": 1.000277, "water": 1.3330, "glass": 1.925, "diamond": 2.42}
        newdata = dict()
        for ray in self.view.get_initial_rays():
            line = glassmath.refract(ray, self.glass.first_normal, self.glass.first_points,
                refr_indexes["air"], refr_indexes["glass"])
            # print "line1:", line
            line = glassmath.refract(line, self.glass.second_normal, self.glass.second_points,
                refr_indexes["glass"], refr_indexes["air"])
            # print "line2:", line
            p = glassmath.get_line_intersection_with_plane(line,
                self.img.points, self.img.normal)
            # print "p:", p
            view_x = ray[1][0] - self.view.x_offset
            view_y = ray[1][1] - self.view.y_offset
            x = p[0]
            y = p[1]
            view_coord = int(view_y * self.view.width + view_x)
            coord = int(y * self.img.width + x)
            if coord >= 0 and coord < len(self.img.pixlist) and \
            x >= 0 and x < self.img.width:
                newdata[view_coord] = self.img.pixlist[coord]
            else:
                newdata[view_coord] = (0, 0, 0)

        datalist = list()
        for k in sorted(newdata):
            datalist.append(newdata[k])

        new_img = Image.new("RGB", (self.view.width, self.view.height))
        new_img.putdata(datalist)
        new_img.save(filename)
