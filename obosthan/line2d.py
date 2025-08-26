# Copyright (c) 2018-2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details


"""
2D line object
"""

from math import sin, cos, radians, dist, sqrt
from .point2d import OPoint2D

class OLine2D:
    """
    A definite line object in 2D space
    Instance variable such as length contains length of the line.
    """

    def __init__(self, _x1, _y1, _x2, _y2):
        self.__coord = [_x1, _y1, _x2, _y2]
        self.__length = self.__cal_length()

    def __cal_length(self):
        return (((self.__coord[2]-self.__coord[0])**2) + ((self.__coord[3]-self.__coord[1])**2))**0.5

    @property
    def length(self):
        return self.__length

    def copy(self):
        """
        Returns a copy of the line object
        """

        return OLine2D(self.__coord[0], self.__coord[1], self.__coord[2], self.__coord[3])

    def get_points(self):
        """
        Returns end points of the line as two points in a tuple
        """

        return (OPoint2D(self.__coord[0], self.__coord[1]), OPoint2D(self.__coord[2], self.__coord[3]))

    def distance_to_point(self, point):
        """
        Returns perpendicular distance to a point
        """

        tri_a = dist((self.__coord[0], self.__coord[1]), point)
        tri_b = dist((self.__coord[0], self.__coord[1]), (self.__coord[2], self.__coord[3]))
        tri_c = dist((self.__coord[2], self.__coord[3]), point)
        semp = (tri_a + tri_b + tri_c) / 2
        area = sqrt(semp * (semp - tri_a) * (semp - tri_b) * (semp - tri_c))

        if tri_b != 0:
            return (2 * area) / tri_b
        else:
            return None

    def translate(self, x, y):
        """
        Moves the line in space along X and Y axes by amounts defined by x and y arguments
        """

        self.__coord[0] = self.__coord[0] + x
        self.__coord[1] = self.__coord[1] + y
        self.__coord[2] = self.__coord[2] + x
        self.__coord[3] = self.__coord[3] + y

    def rotate_centroid(self, angle):
        """
        Rotates the polygon by degrees about it's centroid
        """

        old_centroid = (((self.__coord[2]-self.__coord[0])/2)+self.__coord[0], ((self.__coord[3]-self.__coord[1])/2)+self.__coord[1])

        self.translate(-old_centroid[0], -old_centroid[1])

        old_coord_x = self.__coord[0]
        old_coord_y = self.__coord[1]
        self.__coord[0] = (cos(radians(angle)) * old_coord_x) - (sin(radians(angle)) * old_coord_y)
        self.__coord[1] = (sin(radians(angle)) * old_coord_x) + (cos(radians(angle)) * old_coord_y)
        old_coord_x = self.__coord[2]
        old_coord_y = self.__coord[3]
        self.__coord[2] = (cos(radians(angle)) * old_coord_x) - (sin(radians(angle)) * old_coord_y)
        self.__coord[3] = (sin(radians(angle)) * old_coord_x) + (cos(radians(angle)) * old_coord_y)

        self.translate(old_centroid[0], old_centroid[1])

    def rotate_point(self, angle, point):
        """
        Rotates the polygon by degrees about a defined point
        """

        if type(point) is tuple or type(point) is list or type(point) is OPoint2D:

            if len(point) == 2:

                origin = (point[0], point[1])
                self.translate(-origin[0], -origin[1])

                old_coord_x = self.__coord[0]
                old_coord_y = self.__coord[1]
                self.__coord[0] = (cos(radians(angle)) * old_coord_x) - (sin(radians(angle)) * old_coord_y)
                self.__coord[1] = (sin(radians(angle)) * old_coord_x) + (cos(radians(angle)) * old_coord_y)
                old_coord_x = self.__coord[2]
                old_coord_y = self.__coord[3]
                self.__coord[2] = (cos(radians(angle)) * old_coord_x) - (sin(radians(angle)) * old_coord_y)
                self.__coord[3] = (sin(radians(angle)) * old_coord_x) + (cos(radians(angle)) * old_coord_y)

                self.translate(origin[0], origin[1])

    def transform(self, matrix):
        """
        Applies a matrix transformation to the line vertices about it's centroid
        """

        if type(matrix) is tuple or type(matrix) is list:

            if len(matrix) == 4:

                old_centroid = (((self.__coord[2] - self.__coord[0]) / 2) + self.__coord[0], ((self.__coord[3] - self.__coord[1]) / 2) + self.__coord[1])

                self.translate(-old_centroid[0], -old_centroid[1])

                old_point = (self.__coord[0], self.__coord[1])
                self.__coord[0] = (old_point[0] * matrix[0]) + (old_point[1] * matrix[1])
                self.__coord[1] = (old_point[0] * matrix[2]) + (old_point[1] * matrix[3])
                old_point = (self.__coord[2], self.__coord[3])
                self.__coord[2] = (old_point[0] * matrix[0]) + (old_point[1] * matrix[1])
                self.__coord[3] = (old_point[0] * matrix[2]) + (old_point[1] * matrix[3])

                self.translate(old_centroid[0], old_centroid[1])

    def transform_point(self, matrix, point):
        """
        Applies a matrix transformation to the line vertices about a defined point
        """

        if (type(matrix) is tuple or type(matrix) is list) and (type(point) is tuple or type(point) is list or type(point) is OPoint2D):

            if len(matrix) == 4 and len(point) == 2:

                old_centroid = (point[0], point[1])

                self.translate(-old_centroid[0], -old_centroid[1])

                old_point = (self.__coord[0], self.__coord[1])
                self.__coord[0] = (old_point[0] * matrix[0]) + (old_point[1] * matrix[1])
                self.__coord[1] = (old_point[0] * matrix[2]) + (old_point[1] * matrix[3])
                old_point = (self.__coord[2], self.__coord[3])
                self.__coord[2] = (old_point[0] * matrix[0]) + (old_point[1] * matrix[1])
                self.__coord[3] = (old_point[0] * matrix[2]) + (old_point[1] * matrix[3])

                self.translate(old_centroid[0], old_centroid[1])

    def scale(self, x, y):
        """
        Applies a scale transformation to the line vertices about it's centroid
        """

        old_centroid = (((self.__coord[2] - self.__coord[0]) / 2) + self.__coord[0], ((self.__coord[3] - self.__coord[1]) / 2) + self.__coord[1])

        self.translate(-old_centroid[0], -old_centroid[1])

        old_point = (self.__coord[0], self.__coord[1])
        self.__coord[0] = (old_point[0] * x) + (old_point[1] * 0)
        self.__coord[1] = (old_point[0] * 0) + (old_point[1] * y)
        old_point = (self.__coord[2], self.__coord[3])
        self.__coord[2] = (old_point[0] * x) + (old_point[1] * 0)
        self.__coord[3] = (old_point[0] * 0) + (old_point[1] * y)

        self.translate(old_centroid[0], old_centroid[1])

    def scale_point(self, x, y, point):
        """
        Applies a scale transformation to the line vertices about a defined point
        """

        if type(point) is tuple or type(point) is list or type(point) is OPoint2D:

            if len(point) == 2:

                old_centroid = (point[0], point[1])

                self.translate(-old_centroid[0], -old_centroid[1])

                old_point = (self.__coord[0], self.__coord[1])
                self.__coord[0] = (old_point[0] * x) + (old_point[1] * 0)
                self.__coord[1] = (old_point[0] * 0) + (old_point[1] * y)
                old_point = (self.__coord[2], self.__coord[3])
                self.__coord[2] = (old_point[0] * x) + (old_point[1] * 0)
                self.__coord[3] = (old_point[0] * 0) + (old_point[1] * y)

                self.translate(old_centroid[0], old_centroid[1])

    def shear(self, x, y):
        """
        Applies a shear transformation to the line vertices about it's centroid
        """

        old_centroid = (((self.__coord[2] - self.__coord[0]) / 2) + self.__coord[0], ((self.__coord[3] - self.__coord[1]) / 2) + self.__coord[1])

        self.translate(-old_centroid[0], -old_centroid[1])

        old_point = (self.__coord[0], self.__coord[1])
        self.__coord[0] = (old_point[0] * 1) + (old_point[1] * x)
        self.__coord[1] = (old_point[0] * y) + (old_point[1] * 1)
        old_point = (self.__coord[2], self.__coord[3])
        self.__coord[2] = (old_point[0] * 1) + (old_point[1] * x)
        self.__coord[3] = (old_point[0] * y) + (old_point[1] * 1)

        self.translate(old_centroid[0], old_centroid[1])

    def shear_point(self, x, y, point):
        """
        Applies a shear transformation to the line vertices about a defined point
        """

        if type(point) is tuple or type(point) is list or type(point) is OPoint2D:

            if len(point) == 2:

                old_centroid = (point[0], point[1])

                self.translate(-old_centroid[0], -old_centroid[1])

                old_point = (self.__coord[0], self.__coord[1])
                self.__coord[0] = (old_point[0] * 1) + (old_point[1] * x)
                self.__coord[1] = (old_point[0] * y) + (old_point[1] * 1)
                old_point = (self.__coord[2], self.__coord[3])
                self.__coord[2] = (old_point[0] * 1) + (old_point[1] * x)
                self.__coord[3] = (old_point[0] * y) + (old_point[1] * 1)

                self.translate(old_centroid[0], old_centroid[1])

    def __iter__(self):
        return iter(self.__coord)

    def __setitem__(self, i, val):
        if type(val) is float or type(val) is int:
            self.__coord[i] = val
        elif type(val) is OLine2D or (type(val) is list and len(val) == 4):
            self.__coord[0] = val[0]
            self.__coord[1] = val[1]
            self.__coord[2] = val[2]
            self.__coord[3] = val[3]
        else:
            return self

        self.__length = (((self.__coord[2]-self.__coord[0])**2) + ((self.__coord[3]-self.__coord[1])**2))**0.5

    def __getitem__(self, i):
        return self.__coord[i]

    def __len__(self):
        return len(self.__coord)

    def __repr__(self):
        return str(self.__coord)
