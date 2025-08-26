# Copyright (c) 2023, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details


"""
Surface object
"""

from math import cos, sin, radians
from .point3d import OPoint3D


class OSurface:
    """
    A surface object which can be used for storing a surface vertices.
    Instance variables such as num_of_points, centroid tell number of vertices and centroid coordinate respectively.
    """

    def __init__(self, points):
        self.__coord_list = []
        self.__num_of_points = 0
        self.add_points(points)
        self.__centroid = self.__cal_centroid()

    @property
    def num_of_points(self):
        return self.__num_of_points

    @property
    def centroid(self):
        return self.__centroid

    def add_points(self, points):
        """
        Adds points into the surface
        """

        if type(points) is list or type(points) is tuple:
            if len(points) > 0:
                for point in points:
                    self.__coord_list.append(OPoint3D(point[0], point[1], point[2]))
                self.__num_of_points = len(self.__coord_list)
                self.__centroid = self.__cal_centroid()

    def add_point(self, _x, _y, _z):
        """
        Adds a single point into the polygon
        """

        if _x is not None and _y is not None:
            self.__coord_list.append(OPoint3D(_x, _y, _z))
            self.__num_of_points = len(self.__coord_list)
            self.__centroid = self.__cal_centroid()

    def remove_point(self, point):
        """
        Removes an existing point from the polygon
        """

        if type(point) is list or type(point) is tuple:
            val = OPoint3D(point[0], point[1], point[2])
            if val in self.__coord_list:
                self.__coord_list.remove(val)
                self.__num_of_points = len(self.__coord_list)
                self.__centroid = self.__cal_centroid()
        elif type(point) is OPoint3D:
            if point in self.__coord_list:
                self.__coord_list.remove(point)
                self.__num_of_points = len(self.__coord_list)
                self.__centroid = self.__cal_centroid()

    def get_point(self, i):
        """
        Returns an existing point from the polygon defined by index
        """

        return (self.__coord_list[i][0], self.__coord_list[i][1], self.__coord_list[i][2])

    @property
    def coords(self):
        """
        Returns the polygon points
        """

        return tuple(self.__coord_list)

    def __iter__(self):
        return iter(self.__coord_list)

    def __setitem__(self, i, val):
        if type(val) is list or type(val) is OPoint3D:
            self.__coord_list[i][0] = val[0]
            self.__coord_list[i][1] = val[1]
            self.__coord_list[i][2] = val[2]
            self.__num_of_points = len(self.__coord_list)
            self.__centroid = self.__cal_centroid()
        else:
            return self

    def __len__(self):
        return self.__num_of_points

    def __repr__(self):
        return str(self.__coord_list)

    def get_range(self):
        """
        Returns range of surface vertices
        """

        if self.__num_of_points != 0:

            x_coords = []
            y_coords = []
            z_coords = []

            for coord_x, coord_y, coord_z in self.__coord_list:
                x_coords.append(coord_x)
                y_coords.append(coord_y)
                z_coords.append(coord_z)

            xcoord_min = min(x_coords)
            xcoord_max = max(x_coords)
            ycoord_min = min(y_coords)
            ycoord_max = max(y_coords)
            zcoord_min = min(z_coords)
            zcoord_max = max(z_coords)

            aabb = [[xcoord_min, xcoord_max], [ycoord_min, ycoord_max], [zcoord_min, zcoord_max]]

            return aabb

        else:
            return None

    def __cal_centroid(self):

        if self.__num_of_points != 0:

            cen_x = 0
            cen_y = 0
            cen_z = 0
            for coord_x, coord_y, coord_z in self.__coord_list:
                cen_x = cen_x + coord_x
                cen_y = cen_y + coord_y
                cen_z = cen_z + coord_z

            return OPoint3D(cen_x / self.__num_of_points, cen_y / self.__num_of_points, cen_z / self.__num_of_points)

        else:
            return None

    def translate(self, x, y, z):
        """
        Moves the surface in space along X, Y and Z axes by amounts defined by x, y and z arguments
        """

        for i in range(self.__num_of_points):
            self.__coord_list[i][0] = self.__coord_list[i][0] + x
            self.__coord_list[i][1] = self.__coord_list[i][1] + y
            self.__coord_list[i][2] = self.__coord_list[i][2] + z

        self.__centroid = self.__cal_centroid()

    def transform(self, matrix):
        """
        Applies a matrix transformation to the surface vertices about its centroid
        """

        if type(matrix) is tuple or type(matrix) is list:

            if len(matrix) == 9:

                old_centroid = (self.__centroid[0], self.__centroid[1], self.__centroid[2])

                self.translate(-old_centroid[0], -old_centroid[1], -old_centroid[2])

                for i in range(self.__num_of_points):
                    old_point = (self.__coord_list[i][0], self.__coord_list[i][1], self.__coord_list[i][2])
                    self.__coord_list[i][0] = (old_point[0] * matrix[0]) + (old_point[1] * matrix[1]) + (old_point[2] * matrix[2])
                    self.__coord_list[i][1] = (old_point[0] * matrix[3]) + (old_point[1] * matrix[4]) + (old_point[2] * matrix[5])
                    self.__coord_list[i][2] = (old_point[0] * matrix[6]) + (old_point[1] * matrix[7]) + (old_point[1] * matrix[8])

                self.translate(old_centroid[0], old_centroid[1], old_centroid[2])

                self.__centroid = self.__cal_centroid()

    def transform_point(self, matrix, point):
        """
        Applies a matrix transformation to the surface vertices about a defined point
        """

        if (type(matrix) is list or type(matrix) is tuple) and (type(point) is tuple or type(point) is list or type(point) is OPoint3D):

            if len(matrix) == 9 and len(point) == 3:

                old_centroid = (point[0], point[1], point[2])

                self.translate(-old_centroid[0], -old_centroid[1], -old_centroid[2])

                for i in range(self.__num_of_points):
                    old_point = (self.__coord_list[i][0], self.__coord_list[i][1], self.__coord_list[i][2])
                    self.__coord_list[i][0] = (old_point[0] * matrix[0]) + (old_point[1] * matrix[1]) + (old_point[2] * matrix[2])
                    self.__coord_list[i][1] = (old_point[0] * matrix[3]) + (old_point[1] * matrix[4]) + (old_point[2] * matrix[5])
                    self.__coord_list[i][2] = (old_point[0] * matrix[6]) + (old_point[1] * matrix[7]) + (old_point[1] * matrix[8])

                self.translate(old_centroid[0], old_centroid[1], old_centroid[2])

                self.__centroid = self.__cal_centroid()

    def scale(self, x, y, z):
        """
        Scale the surface vertices about its centroid
        """

        old_centroid = (self.__centroid[0], self.__centroid[1], self.__centroid[2])

        self.translate(-old_centroid[0], -old_centroid[1], -old_centroid[2])

        for i in range(self.__num_of_points):
            old_point = (self.__coord_list[i][0], self.__coord_list[i][1], self.__coord_list[i][2])
            self.__coord_list[i][0] = old_point[0] * x
            self.__coord_list[i][1] = old_point[1] * y
            self.__coord_list[i][2] = old_point[2] * z

        self.translate(old_centroid[0], old_centroid[1], old_centroid[2])

        self.__centroid = self.__cal_centroid()

    def scale_point(self, x, y, z, point):
        """
        Scale the surface vertices about a defined point
        """

        if type(point) is tuple or type(point) is list or type(point) is OPoint3D:

            if len(point) == 3:

                old_centroid = (point[0], point[1], point[2])

                self.translate(-old_centroid[0], -old_centroid[1], -old_centroid[2])

                for i in range(self.__num_of_points):
                    old_point = (self.__coord_list[i][0], self.__coord_list[i][1], self.__coord_list[i][2])
                    self.__coord_list[i][0] = old_point[0] * x
                    self.__coord_list[i][1] = old_point[1] * y
                    self.__coord_list[i][2] = old_point[2] * z

                self.translate(old_centroid[0], old_centroid[1], old_centroid[2])

                self.__centroid = self.__cal_centroid()

    def shear(self, xy, yx, xz, zx, yz, zy):
        """
        Shear the surface vertices about its centroid
        """

        old_centroid = (self.__centroid[0], self.__centroid[1], self.__centroid[2])

        self.translate(-old_centroid[0], -old_centroid[1], -old_centroid[2])

        for i in range(self.__num_of_points):
            old_point = (self.__coord_list[i][0], self.__coord_list[i][1], self.__coord_list[i][2])
            self.__coord_list[i][0] = old_point[0] + (old_point[1] * yx) + (old_point[2] * zx)
            self.__coord_list[i][1] = (old_point[0] * xy) + old_point[1] + (old_point[2] * zy)
            self.__coord_list[i][2] = (old_point[0] * xz) + (old_point[1] * yz) + old_point[2]

        self.translate(old_centroid[0], old_centroid[1], old_centroid[2])

        self.__centroid = self.__cal_centroid()

    def shear_point(self, xy, yx, xz, zx, yz, zy, point):
        """
        Shear the surface vertices about a defined point
        """

        if type(point) is tuple or type(point) is list or type(point) is OPoint3D:

            if len(point) == 3:

                old_centroid = (point[0], point[1], point[2])

                self.translate(-old_centroid[0], -old_centroid[1], -old_centroid[2])

                for i in range(self.__num_of_points):
                    old_point = (self.__coord_list[i][0], self.__coord_list[i][1], self.__coord_list[i][2])
                    self.__coord_list[i][0] = old_point[0] + (old_point[1] * yx) + (old_point[2] * zx)
                    self.__coord_list[i][1] = (old_point[0] * xy) + old_point[1] + (old_point[2] * zy)
                    self.__coord_list[i][2] = (old_point[0] * xz) + (old_point[1] * yz) + old_point[2]

                self.translate(old_centroid[0], old_centroid[1], old_centroid[2])

                self.__centroid = self.__cal_centroid()

    def rotate_centroid(self, angle_x, angle_y, angle_z):
        """
        Rotates the surface by degrees about its centroid
        """

        old_centroid = (self.__centroid[0], self.__centroid[1], self.__centroid[2])

        self.translate(-old_centroid[0], -old_centroid[1], -old_centroid[2])

        if angle_x != 0:

            for coord_i in range(self.__num_of_points):
                old_coord_x = self.__coord_list[coord_i][0]
                old_coord_y = self.__coord_list[coord_i][1]
                old_coord_z = self.__coord_list[coord_i][2]
                self.__coord_list[coord_i][0] = old_coord_x
                self.__coord_list[coord_i][1] = (cos(radians(angle_x)) * old_coord_y) - (sin(radians(angle_x)) * old_coord_z)
                self.__coord_list[coord_i][2] = (sin(radians(angle_x)) * old_coord_y) + (cos(radians(angle_x)) * old_coord_z)

        if angle_y != 0:

            for coord_i in range(self.__num_of_points):
                old_coord_x = self.__coord_list[coord_i][0]
                old_coord_y = self.__coord_list[coord_i][1]
                old_coord_z = self.__coord_list[coord_i][2]
                self.__coord_list[coord_i][0] = (cos(radians(angle_y)) * old_coord_x) + (sin(radians(angle_y)) * old_coord_z)
                self.__coord_list[coord_i][1] = old_coord_y
                self.__coord_list[coord_i][2] = -(sin(radians(angle_y)) * old_coord_x) + (cos(radians(angle_y)) * old_coord_z)

        if angle_z != 0:

            for coord_i in range(self.__num_of_points):
                old_coord_x = self.__coord_list[coord_i][0]
                old_coord_y = self.__coord_list[coord_i][1]
                old_coord_z = self.__coord_list[coord_i][2]
                self.__coord_list[coord_i][0] = (cos(radians(angle_z)) * old_coord_x) - (sin(radians(angle_z)) * old_coord_y)
                self.__coord_list[coord_i][1] = (sin(radians(angle_z)) * old_coord_x) + (cos(radians(angle_z)) * old_coord_y)
                self.__coord_list[coord_i][2] = old_coord_z

        self.translate(old_centroid[0], old_centroid[1], old_centroid[2])

    def rotate_point(self, angle_x, angle_y, angle_z, point):
        """
        Rotates the surface by degrees about a defined point
        """

        if type(point) is tuple or type(point) is list or type(point) is OPoint3D:

            if len(point) == 3:

                origin = (point[0], point[1], point[2])
                self.translate(-origin[0], -origin[1], -origin[2])

                if angle_x != 0:

                    for coord_i in range(self.__num_of_points):
                        old_coord_x = self.__coord_list[coord_i][0]
                        old_coord_y = self.__coord_list[coord_i][1]
                        old_coord_z = self.__coord_list[coord_i][2]
                        self.__coord_list[coord_i][0] = old_coord_x
                        self.__coord_list[coord_i][1] = (cos(radians(angle_x)) * old_coord_y) - (
                                    sin(radians(angle_x)) * old_coord_z)
                        self.__coord_list[coord_i][2] = (sin(radians(angle_x)) * old_coord_y) + (
                                    cos(radians(angle_x)) * old_coord_z)

                if angle_y != 0:

                    for coord_i in range(self.__num_of_points):
                        old_coord_x = self.__coord_list[coord_i][0]
                        old_coord_y = self.__coord_list[coord_i][1]
                        old_coord_z = self.__coord_list[coord_i][2]
                        self.__coord_list[coord_i][0] = (cos(radians(angle_y)) * old_coord_x) + (
                                    sin(radians(angle_y)) * old_coord_z)
                        self.__coord_list[coord_i][1] = old_coord_y
                        self.__coord_list[coord_i][2] = -(sin(radians(angle_y)) * old_coord_x) + (
                                    cos(radians(angle_y)) * old_coord_z)

                if angle_z != 0:

                    for coord_i in range(self.__num_of_points):
                        old_coord_x = self.__coord_list[coord_i][0]
                        old_coord_y = self.__coord_list[coord_i][1]
                        old_coord_z = self.__coord_list[coord_i][2]
                        self.__coord_list[coord_i][0] = (cos(radians(angle_z)) * old_coord_x) - (
                                    sin(radians(angle_z)) * old_coord_y)
                        self.__coord_list[coord_i][1] = (sin(radians(angle_z)) * old_coord_x) + (
                                    cos(radians(angle_z)) * old_coord_y)
                        self.__coord_list[coord_i][2] = old_coord_z

                self.translate(origin[0], origin[1], origin[2])
                self.__centroid = self.__cal_centroid()
