# Copyright (c) 2018-2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details


"""
2D vector object
"""

from math import sin, cos, radians, acos, degrees, atan

class OVector2D:
    """
    A vector object which can be used for vector calculations as well as to find general vector properties.
    Instance variables such as length, unit, and angle contain length of the vector, unit vector, and
    absolute angle of the vector between 0 and 360 degrees respectively.
    """

    def __init__(self, _x, _y):
        self.__coord = [_x, _y]
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
        return ((self.__coord[0]**2) + (self.__coord[1]**2))**0.5

    def __cal_unit(self):
        if self.__length == 0:
            return [0, 0]
        else:
            return [self.__coord[0] / self.__length, self.__coord[1] / self.__length]

    def __cal_angle(self):
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

    def copy(self):
        """
        Returns a copy of the vector object
        """

        return OVector2D(self.__coord[0], self.__coord[1])

    def define_line(self, x1, y1, x2, y2):
        """
        Alters the vector to follow a line as defined by two end points (x1, y1) and (x2, y22)
        """

        self.__coord[0] = x2 - x1
        self.__coord[1] = y2 - y1
        self.__length = self.__cal_length()
        self.__x_axis = self.__cal_x_axis()
        self.__unit = self.__cal_unit()
        self.__angle = self.__cal_angle()

    def define_line1(self, x1, y1, x2, y2):
        """
        Alters the vector to follow a line as defined by two end points (x1, y1) and (x2, y22) and always orients the vector in positive direction
        """

        if x2 > x1:
            self.__coord[0] = x2 - x1
        else:
            self.__coord[0] = x1 - x2

        if y2 > y1:
            self.__coord[1] = y2 - y1
        else:
            self.__coord[1] = y1 - y2

        self.__length = self.__cal_length()
        self.__x_axis = self.__cal_x_axis()
        self.__unit = self.__cal_unit()
        self.__angle = self.__cal_angle()

    def define_polar(self, length, angle):
        """
        Alters the vector to a specified length and angle (degrees)
        """

        self.__coord[0] = length * cos(radians(angle))
        self.__coord[1] = length * sin(radians(angle))
        self.__length = self.__cal_length()
        self.__x_axis = self.__cal_x_axis()
        self.__unit = self.__cal_unit()
        self.__angle = self.__cal_angle()

    def project(self, other):
        """
        Projects another vector and return projected vector
        """

        if self.__length != 0:
            vector_length = self.dot(other)/self.__length
        return OVector2D(self.__unit[0]*vector_length, self.__unit[1]*vector_length)

    def dot(self, other):
        return (self.__coord[0]*other[0]) + (self.__coord[1]*other[1])

    def angle_to(self, other):
        """
        Finds angle to another vector in degrees
        """

        denominator = self.__length*other.length
        if denominator != 0.0:
            try:
                ratio = self.dot(other)/denominator
                return degrees(acos(ratio))
            except:
                return 180.0
        else:
            return 180.0

    def rotate(self, angle):
        """
        Rotates the vector to a specified angle in degrees (anticlockwise)
        """

        self.__coord[0] = (cos(radians(angle)) * self.__x_axis[0]) - (sin(radians(angle)) * self.__x_axis[1])
        self.__coord[1] = (sin(radians(angle)) * self.__x_axis[0]) + (cos(radians(angle)) * self.__x_axis[1])
        self.__unit = self.__cal_unit()
        self.__angle = self.__cal_angle()

    def rotate_to(self, angle):
        """
        Rotates the vector by specified angle in degrees (anticlockwise)
        """

        xcoord = self.__coord[0]
        ycoord = self.__coord[1]
        self.__coord[0] = (cos(radians(angle)) * xcoord) - (sin(radians(angle)) * ycoord)
        self.__coord[1] = (sin(radians(angle)) * xcoord) + (cos(radians(angle)) * ycoord)
        self.__unit = self.__cal_unit()
        self.__angle = self.__cal_angle()

    def negate(self):
        """
        Negates the vector
        """

        self.__coord[0] = -self.__coord[0]
        self.__coord[1] = -self.__coord[1]
        self.__unit = self.__cal_unit()

    def scale(self, magnitude):
        """
        Scales the vector by to a specified factor
        """

        if type(magnitude) is float or type(magnitude) is int:
            self.__coord[0] = self.__coord[0] * magnitude
            self.__coord[1] = self.__coord[1] * magnitude
            self.__length = ((self.__coord[0]**2) + (self.__coord[1]**2))**0.5
            self.__x_axis = [self.__length, 0]

    def ortho_left(self):
        """
        Returns a perpendicular vector
        """

        return OVector2D(self.__coord[1], -self.__coord[0])

    def ortho_right(self):
        """
        Returns a perpendicular vector
        """

        return OVector2D(-self.__coord[1], self.__coord[0])

    def __iter__(self):
        return iter(self.__coord)

    def __setitem__(self, i, val):
        if type(val) is float or type(val) is int:
            self.__coord[i] = val
        elif type(val) is OVector2D or (type(val) is list and len(val) == 2):
            self.__coord[0] = val[0]
            self.__coord[1] = val[1]
        else:
            return self

        self.__length = ((self.__coord[0]**2)+(self.__coord[1]**2))**0.5
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
            return OVector2D(self.__coord[0] + other, self.__coord[1] + other)
        elif type(other) is OVector2D or (type(other) is list and len(other) == 2):
            return OVector2D(self.__coord[0]+other[0], self.__coord[1]+other[1])
        else:
            return self

    def __sub__(self, other):
        if type(other) is float or type(other) is int:
            return OVector2D(self.__coord[0] - other, self.__coord[1] - other)
        elif type(other) is OVector2D or (type(other) is list and len(other) == 2):
            return OVector2D(self.__coord[0]-other[0], self.__coord[1]-other[1])
        else:
            return self

    def __neg__(self):
        return OVector2D(-self.__coord[0], -self.__coord[1])

    def __mul__(self, other):
        if type(other) is float or type(other) is int:
            return OVector2D(self.__coord[0]*other, self.__coord[1]*other)
        elif type(other) is OVector2D or (type(other) is list and len(other) == 2):
            return (self.__coord[0]*other[1]) - (self.__coord[1]*other[0])
        else:
            return self

    def __truediv__(self, fac):
        if type(fac) is float or type(fac) is int:
            if fac != 0:
                return OVector2D(self.__coord[0]/fac, self.__coord[1]/fac)
            else:
                return self
        else:
            return self
