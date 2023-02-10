# Copyright (c) 2023, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details


"""
3D point object
"""

from math import degrees, atan

class OPoint3D:
    """
    A point object can be used for storing a 3D point coordinate as well as finding distances to other points,
    calculating new points in space for a given vector. Instance variables such as distance, and heading contain distance to origin,
    and absolute angle of the vector made from the point which lies between 0 and 360 degrees respectively.
    """

    def __init__(self, _x, _y, _z):
        self.__coord = [_x, _y, _z]
        self.__distance = self.__cal_distance()
        self.__xy_axes = self.__cal_xy_axes()
        self.__heading = self.__cal_heading()

    def __cal_distance(self):
        return ((self.__coord[0]**2)+(self.__coord[1]**2)+(self.__coord[2]**2))**0.5

    def __cal_xy_axes(self):
        return [(self.__distance, 0), (self.__distance, 0)]

    def __cal_heading(self):

        xy_plane = 0.0
        yz_plane = 0.0
        xz_plane = 0.0

        if (self.__coord[1] == 0 and self.__coord[0] == 0.0):
            xy_plane = 0.0
        elif (self.__coord[1] > 0 and self.__coord[0] == 0.0):
            xy_plane = 90.0
        elif (self.__coord[1] < 0 and self.__coord[0] == 0.0):
            xy_plane = 270.0
        elif (self.__coord[0] < 0):
            xy_plane = 180 + degrees(atan(self.__coord[1] / self.__coord[0]))
        elif (self.__coord[0] > 0 and self.__coord[1] < 0):
            xy_plane = 360 + degrees(atan(self.__coord[1]/self.__coord[0]))
        else:
            xy_plane = degrees(atan(self.__coord[1] / self.__coord[0]))

        if (self.__coord[2] == 0 and self.__coord[1] == 0.0):
            yz_plane = 0.0
        elif (self.__coord[2] > 0 and self.__coord[1] == 0.0):
            yz_plane = 90.0
        elif (self.__coord[2] < 0 and self.__coord[1] == 0.0):
            yz_plane = 270.0
        elif (self.__coord[1] < 0):
            yz_plane = 180 + degrees(atan(self.__coord[2] / self.__coord[1]))
        elif (self.__coord[1] > 0 and self.__coord[2] < 0):
            yz_plane = 360 + degrees(atan(self.__coord[2]/self.__coord[1]))
        else:
            yz_plane = degrees(atan(self.__coord[2] / self.__coord[1]))

        if (self.__coord[2] == 0 and self.__coord[0] == 0.0):
            xz_plane = 0.0
        elif (self.__coord[2] > 0 and self.__coord[0] == 0.0):
            xz_plane = 90.0
        elif (self.__coord[2] < 0 and self.__coord[0] == 0.0):
            xz_plane = 270.0
        elif (self.__coord[0] < 0):
            xz_plane = 180 + degrees(atan(self.__coord[2] / self.__coord[0]))
        elif (self.__coord[0] > 0 and self.__coord[2] < 0):
            xz_plane = 360 + degrees(atan(self.__coord[2]/self.__coord[0]))
        else:
            xz_plane = degrees(atan(self.__coord[2] / self.__coord[0]))

        return [xy_plane, yz_plane, xz_plane]

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

        return OPoint3D(self.__coord[0], self.__coord[1], self.__coord[2])

    def distance_to(self, other):
        """
        Finds distance to another point
        """

        if type(other) is list or type(other) is OPoint3D:
            return (((other[0] - self.__coord[0])**2) + ((other[1] - self.__coord[1])**2) + ((other[2] - self.__coord[2])**2))**0.5
        else:
            return None

    def __str__(self):
        return "X: " + str(self.__coord[0]) + ", Y: " + str(self.__coord[1]) + ", Z: " + str(self.__coord[2])

    def __iter__(self):
        return iter(self.__coord)

    def __setitem__(self, i, val):
        if type(val) is float or type(val) is int:
            self.__coord[i] = val
        elif type(val) is OPoint3D or type(val) is list:
            self.__coord[0] = val[0]
            self.__coord[1] = val[1]
            self.__coord[2] = val[2]
        else:
            return self

        self.__distance = self.__cal_distance()
        self.__xy_axes = self.__cal_xy_axes()
        self.__heading = self.__cal_heading()

    def __getitem__(self, i):
        return self.__coord[i]

    def __len__(self):
        return len(self.__coord)

    def __repr__(self):
        return str(self.__coord)

    def __add__(self, fac):
        if type(fac) is float or type(fac) is int:
            return OPoint3D(self.__coord[0] + fac, self.__coord[1] + fac, self.__coord[2] + fac)
        else:
            return self

    def __sub__(self, fac):
        if type(fac) is float or type(fac) is int:
            return OPoint3D(self.__coord[0] - fac, self.__coord[1] - fac, self.__coord[2] - fac)
        else:
            return self

    def __neg__(self):
        return OPoint3D(-self.__coord[0], -self.__coord[1])

    def __mul__(self, fac):
        if type(fac) is float or type(fac) is int:
            return OPoint3D(self.__coord[0]*fac, self.__coord[1]*fac)
        else:
            return self

    def __truediv__(self, fac):
        if type(fac) is float or type(fac) is int:
            if fac != 0:
                return OPoint3D(self.__coord[0]/fac, self.__coord[1]/fac, self.__coord[2]/fac)
            else:
                return self
        else:
            return self
