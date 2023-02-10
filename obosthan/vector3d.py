# Copyright (c) 2023, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details


"""
3D vector object
"""

from math import sin, cos, radians, acos, degrees, atan

class OVector3D:
    """
    A vector object which can be used for vector calculations as well as to find general vector properties.
    Instance variables such as length, unit, and angle contain length of the vector, unit vector, and
    absolute angle of the vector between 0 and 360 degrees respectively.
    """

    def __init__(self, _x, _y, _z):
        self.__coord = [_x, _y, _z]
        self.__length = self.__cal_length()
        self.__x_axis = self.__cal_x_axis()
        self.__unit = self.__cal_unit()
        self.__angle = self.__cal_angle()

    @property
    def angle(self):
        return self.__angle

    @property
    def unit(self):
        return self.__unit

    @property
    def length(self):
        return self.__length

    def __cal_x_axis(self):
        return [self.__length, 0]

    def __cal_length(self):
        return ((self.__coord[0]**2)+(self.__coord[1]**2)+(self.__coord[2]**2))**2

    def __cal_unit(self):
        if self.__length == 0:
            return [0, 0]
        else:
            return [self.__coord[0] / self.__length, self.__coord[1] / self.__length, self.__coord[2] / self.__length]

    def __cal_angle(self):

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

    def copy(self):
        """
        Returns a copy of the vector object
        """

        return OVector3D(self.__coord[0], self.__coord[1], self.__coord[2])

    def define_line(self, x1, y1, z1, x2, y2, z2):
        """
        Alters the vector to follow a line as defined by two end points (x1, y1) and (x2, y22)
        """

        self.__coord[0] = x2 - x1
        self.__coord[1] = y2 - y1
        self.__coord[3] = z2 - z1
        self.__length = self.__cal_length()
        self.__x_axis = self.__cal_x_axis()
        self.__unit = self.__cal_unit()
        self.__angle = self.__cal_angle()

    def define_polar(self, length, angle1, angle2):
        """
        Alters the vector to a specified length and angle (degrees)
        """

        self.__coord[0] = length * cos(radians(angle2)) * sin(radians(angle1))
        self.__coord[1] = length * cos(radians(angle2)) * cos(radians(angle1))
        self.__coord[2] = length * sin(radians(angle2))
        self.__length = self.__cal_length()
        self.__x_axis = self.__cal_x_axis()
        self.__unit = self.__cal_unit()
        self.__angle = self.__cal_angle()

    def dot(self, other):
        return (self.__coord[0]*other[0]) + (self.__coord[1]*other[1]) + (self.__coord[2]*other[2])

    def angle_to(self, other):
        """
        Finds angle to another vector in degrees
        """

        denominator = self.__length*other.length
        if denominator != 0.0:
            ratio = round(self.dot(other)/denominator, 12)
            return degrees(acos(ratio))
        else:
            return None

    def negate(self):
        """
        Negates the vector
        """

        self.__coord[0] = -self.__coord[0]
        self.__coord[1] = -self.__coord[1]
        self.__coord[2] = -self.__coord[2]
        self.__unit = self.__cal_unit()

    def scale(self, magnitude):
        """
        Scales the vector by to a specified factor
        """

        if type(magnitude) is float or type(magnitude) is int:
            self.__coord[0] = self.__coord[0] * magnitude
            self.__coord[1] = self.__coord[1] * magnitude
            self.__coord[2] = self.__coord[2] * magnitude
            self.__length = ((self.__coord[0]**2)+(self.__coord[1]**2)+(self.__coord[2]**2))**2
            self.__x_axis = [self.__length, 0]

    def __iter__(self):
        return iter(self.__coord)

    def __setitem__(self, i, val):
        if type(val) is float or type(val) is int:
            self.__coord[i] = val
        elif type(val) is OVector3D or (type(val) is list and len(val) == 3):
            self.__coord[0] = val[0]
            self.__coord[1] = val[1]
            self.__coord[2] = val[2]
        else:
            return self

        self.__length = ((self.__coord[0]**2)+(self.__coord[1]**2)+(self.__coord[2]**2))**2
        self.__x_axis = [self.__length, 0]
        self.__unit = self.__cal_unit()
        self.__angle = self.__cal_angle()

    def __getitem__(self, i):
        return self.__coord[i]

    def __len__(self):
        return len(self.__coord)

    def __repr__(self):
        return str(self.__coord)

    def __add__(self, other):
        if type(other) is float or type(other) is int:
            return OVector3D(self.__coord[0] + other, self.__coord[1] + other, self.__coord[2] + other)
        elif type(other) is OVector3D or (type(other) is list and len(other) == 3):
            return OVector3D(self.__coord[0]+other[0], self.__coord[1]+other[1], self.__coord[1]+other[2])
        else:
            return self

    def __sub__(self, other):
        if type(other) is float or type(other) is int:
            return OVector3D(self.__coord[0] - other, self.__coord[1] - other, self.__coord[2] - other)
        elif type(other) is OVector3D or (type(other) is list and len(other) == 3):
            return OVector3D(self.__coord[0]-other[0], self.__coord[1]-other[1], self.__coord[1]-other[2])
        else:
            return self

    def __neg__(self):
        return OVector3D(-self.__coord[0], -self.__coord[1], -self.__coord[2])

    def __mul__(self, other):
        if type(other) is float or type(other) is int:
            return OVector3D(self.__coord[0]*other, self.__coord[1]*other, self.__coord[2]*other)
        elif type(other) is OVector3D or (type(other) is list and len(other) == 3):
            return OVector3D((self.__coord[1]*other[2]) - (self.__coord[2]*other[1]), -(self.__coord[0]*other[2]) - (self.__coord[2]*other[0]), (self.__coord[0]*other[1]) - (self.__coord[1]*other[0]))
        else:
            return self

    def __truediv__(self, fac):
        if type(fac) is float or type(fac) is int:
            if fac != 0:
                return OVector3D(self.__coord[0]/fac, self.__coord[1]/fac, self.__coord[2]/fac)
        else:
            return self