# Copyright (c) 2018-2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details


"""
2D point object
"""

from math import sin, cos, radians, degrees, atan

class OPoint2D:
    """
    A point object can be used for storing a 2D point coordinate as well as finding distances to other points,
    calculating new points in space for a given vector. Instance variables such as distance, and heading contain distance to origin,
    and absolute angle of the vector made from the point which lies between 0 and 360 degrees respectively.
    """

    def __init__(self, _x, _y):
        self.__coord = [_x, _y]
        self.__distance = self.__cal_distance()
        self.__x_axis = self.__cal_x_axis()
        self.__heading = self.__cal_heading()

    def __cal_distance(self):
        return ((self.__coord[0]**2)+(self.__coord[1]**2))**0.5

    def __cal_x_axis(self):
        return [self.__distance, 0]

    def __cal_heading(self):
        if (self.__coord[1] == 0 and self.__coord[0] == 0.0):
            return 0.0
        elif (self.__coord[1] > 0 and self.__coord[0] == 0.0):
            return 90.0
        elif (self.__coord[1] < 0 and self.__coord[0] == 0.0):
            return 270.0
        elif (self.__coord[0] < 0):
            return 180 + degrees(atan(self.__coord[1] / self.__coord[0]))
        elif (self.__coord[0] > 0 and self.__coord[1] < 0):
            return 360 + degrees(atan(self.__coord[1]/self.__coord[0]))
        else:
            return degrees(atan(self.__coord[1] / self.__coord[0]))

    @property
    def distance(self):
        return self.__distance

    @property
    def heading(self):
        return self.__heading

    def copy(self):
        """
        Returns a copy of the object
        """

        return OPoint2D(self.__coord[0], self.__coord[1])

    def vector_copy(self, vec, distance):
        """
        Returns a new point which follows a vector and maintains a distance from the point
        """

        return OPoint2D(self.__coord[0] + (distance * cos(radians(vec.angle))), self.__coord[1] + (distance * sin(radians(vec.angle))))

    def distance_to(self, other):
        """
        Finds distance to another point
        """

        if type(other) is list or type(other) is OPoint2D:
            return ((other[0] - self.__coord[0])**2)+((other[1] - self.__coord[1])**2)
        else:
            return None

    def __iter__(self):
        return iter(self.__coord)

    def __setitem__(self, i, val):
        if type(val) is float or type(val) is int:
            self.__coord[i] = val
        elif type(val) is OPoint2D:
            self.__coord[0] = val[0]
            self.__coord[1] = val[1]
        elif type(val) is list:
            self.__coord[0] = val[0]
            self.__coord[1] = val[1]
        else:
            return self

        self.__distance = ((self.__coord[0]**2)+(self.__coord[1]**2))**0.5
        self.__x_axis = [self.__distance, 0]
        self.__heading = self.__cal_heading()

    def __str__(self):
        return "X: " + str(self.__coord[0]) + ", Y: " + str(self.__coord[1])

    def __getitem__(self, i):
        return self.__coord[i]

    def __len__(self):
        return len(self.__coord)

    def __repr__(self):
        return str(self.__coord)

    def __add__(self, fac):
        if type(fac) is float or type(fac) is int:
            return OPoint2D(self.__coord[0] + fac, self.__coord[1] + fac)
        else:
            return self

    def __sub__(self, fac):
        if type(fac) is float or type(fac) is int:
            return OPoint2D(self.__coord[0] - fac, self.__coord[1] - fac)
        else:
            return self

    def __neg__(self):
        return OPoint2D(-self.__coord[0], -self.__coord[1])

    def __mul__(self, fac):
        if type(fac) is float or type(fac) is int:
            return OPoint2D(self.__coord[0]*fac, self.__coord[1]*fac)
        else:
            return self

    def __truediv__(self, fac):
        if type(fac) is float or type(fac) is int:
            if fac != 0:
                return OPoint2D(self.__coord[0]/fac, self.__coord[1]/fac)
            else:
                return self
        else:
            return self
