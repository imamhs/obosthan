# Copyright (c) 2018-2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details


"""
2d line object
"""

from math import hypot, sin, cos, radians, acos, degrees, atan
from .point2d import OPoint2D
from .vector2d import OVector2D

class OLine2D:
    """
    A definite line object in 2D space
    Instance variable such as length contains length of the line.
    """

    def __init__(self, _x1, _y1, _x2, _y2):
        self.__coord = [_x1, _y1, _x2, _y2]
        self.__length = self.__cal_length()

    def __cal_length(self):
        return hypot(self.__coord[2]-self.__coord[0], self.__coord[3]-self.__coord[1])

    @property
    def length(self):
        return self.__length

    def copy(self):
        """
        returns a copy of the line object
        """

        return OLine2D(self.__coord[0], self.__coord[1], self.__coord[2], self.__coord[3])

    def get_points(self):
        """
        returns end points of the line as two points in a tuple
        """

        return (OPoint2D(self.__coord[0], self.__coord[1]), OPoint2D(self.__coord[2], self.__coord[3]))

    def distance_to_point(self, point):
        """
        returns perpendicular distance to a point
        """
        if type(point) is OPoint2D or (type(point) is list and len(point) == 2):
            origin_circle = OPoint2D(point[0] - self.__coord[0], point[1] - self.__coord[1])
            line_vector = OVector2D(0, 0)
            circle_vector = OVector2D(0, 0)
            line_vector.define_line(self.__coord[0], self.__coord[1], self.__coord[2], self.__coord[3])
            circle_vector[0] = origin_circle[0]
            circle_vector[1] = origin_circle[1]
            circle_vector_project = line_vector.project(circle_vector)
            circle_project = OPoint2D(circle_vector_project[0], circle_vector_project[1])
            return circle_project.distance_to(origin_circle)
        else:
            return None

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

        self.__length = self.__cal_length()

    def __getitem__(self, i):
        return self.__coord[i]

    def __len__(self):
        return len(self.__coord)

    def __repr__(self):
        return str(self.__coord)
