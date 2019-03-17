# Copyright (c) 2018-2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details


"""
polygon object
"""

from math import cos, sin, radians
from .point2d import OPoint2D
from .line2d import OLine2D

class OPolygon:
    """
    A polygon object which can be used for storing a polygon vertices.
    Instance variables such as num_of_points, centroid tell number of vertices and centroid coordinate respectively.
    """
	
    def __init__(self, points):
        self.__coord_list = []
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
		adds points into the polygon where points must be ordered in clockwise or anti clockwise fashion for correct caculation of the area formed by the polygon vertices
		"""
		
        if type(points) is list:
            for point in points:
                self.__coord_list.append(OPoint2D(point[0], point[1]))
            self.__num_of_points = len(self.__coord_list)
            self.__centroid = self.__cal_centroid()

    def add_point(self, point):
        """
        adds a single point into the polygon
        """
		
        if type(point) is list:
            self.__coord_list.append(OPoint2D(point[0], point[1]))
            self.__num_of_points = len(self.__coord_list)
            self.__centroid = self.__cal_centroid()
        elif type(point) is OPoint2D:
            self.__coord_list.append(point)
            self.__num_of_points = len(self.__coord_list)
            self.__centroid = self.__cal_centroid()

    def add_side(self, side):
        """
		creates a new side for the polygon where the side is defined by a line having two end points
		"""
		
        if type(side) is OLine2D or (type(side) is list and len(side) == 4):
            self.__coord_list.append(OPoint2D(side[0], side[1]))
            self.__coord_list.append(OPoint2D(side[2], side[3]))
            self.__num_of_points = len(self.__coord_list)
            self.__centroid = self.__cal_centroid()

    def remove_point(self, point):
        """
        removes an existing point from the polygon
        """
		
        if type(point) is list:
            val = OPoint2D(point[0], point[1])
            if val in self.__coord_list:
                self.__coord_list.remove(val)
                self.__num_of_points = len(self.__coord_list)
                self.__centroid = self.__cal_centroid()
        elif type(point) is OPoint2D:
            if point in self.__coord_list:
                self.__coord_list.remove(point)
                self.__num_of_points = len(self.__coord_list)
                self.__centroid = self.__cal_centroid()

    def get_point(self, i):
        """
        returns an existing point from the polygon defined by index
        """
		
        return self.__coord_list[i]

    @property
    def coords(self):
        """
        returns the polygon points
        """
        return list(self.__coord_list)

    def __iter__(self):
        return iter(self.__coord_list)

    def __setitem__(self, i, val):
        if type(val) is list:
            self.__coord_list[i][0] = val[0]
            self.__coord_list[i][1] = val[1]
            self.__num_of_points = len(self.__coord_list)
            self.__centroid = self.__cal_centroid()
        elif type(val) is OPoint2D:
            self.__coord_list[i][0] = val[0]
            self.__coord_list[i][1] = val[1]
            self.__num_of_points = len(self.__coord_list)
            self.__centroid = self.__cal_centroid()

    def __len__(self):
        return self.__num_of_points

    def __repr__(self):
        return str(self.__coord_list)

    def get_AABB(self):
        """
        returns axis aligned bounding box of the polygon as a polygon 
        """

        if self.__num_of_points != 0:

            x_coords = []
            y_coords = []

            for coord_x, coord_y in self.__coord_list:

                x_coords.append(coord_x)
                y_coords.append(coord_y)

            xcoord_min = min(x_coords)
            xcoord_max = max(x_coords)
            ycoord_min = min(y_coords)
            ycoord_max = max(y_coords)

            aabb = OPolygon([[xcoord_min, ycoord_min], [xcoord_max, ycoord_min], [xcoord_max, ycoord_max], [xcoord_min, ycoord_max]])

            return aabb

        else:
            return None

    def __cal_centroid(self):

        if self.__num_of_points != 0:

            cen_x = 0
            cen_y = 0
            for coord_x, coord_y in self.__coord_list:
                cen_x = cen_x + coord_x
                cen_y = cen_y + coord_y

            return OPoint2D(cen_x/self.__num_of_points, cen_y/self.__num_of_points)

        else:
            return None

    def translate(self, x, y):
        """
        moves the polygon in space along X and Y axises by amounts defined by x and y arguments
        """

        coord_i = 0

        for coord_i in range(self.__num_of_points):
            self.__coord_list[coord_i][0] = self.__coord_list[coord_i][0] + x
            self.__coord_list[coord_i][1] = self.__coord_list[coord_i][1] + y

        self.__centroid = self.__cal_centroid()

    def transform(self, matrix):
        """
        applies a matrix transformation to the polygon vectices
        """
		
        if type(matrix) is list:

            if len(matrix) == 4:

                old_centroid = (self.__centroid[0], self.__centroid[1])

                self.translate(-old_centroid[0], -old_centroid[1])

                for i in range(self.__num_of_points):
                    old_point = (self.__coord_list[i][0], self.__coord_list[i][1])
                    self.__coord_list[i][0] = (old_point[0] * matrix[0]) + (old_point[1] * matrix[1])
                    self.__coord_list[i][1] = (old_point[0] * matrix[2]) + (old_point[1] * matrix[3])

                self.translate(old_centroid[0], old_centroid[1])

                self.__centroid = self.__cal_centroid()

    def rotate_centroid(self, angle):
        """
        rotates the polygon by degrees about it's centroid
        """

        old_centroid = (self.__centroid[0], self.__centroid[1])

        self.translate(-old_centroid[0], -old_centroid[1])

        for coord_i in range(self.__num_of_points):
            old_coord_x = self.__coord_list[coord_i][0]
            old_coord_y = self.__coord_list[coord_i][1]
            self.__coord_list[coord_i][0] = (cos(radians(angle)) * old_coord_x) - (sin(radians(angle)) * old_coord_y)
            self.__coord_list[coord_i][1] = (sin(radians(angle)) * old_coord_x) + (cos(radians(angle)) * old_coord_y)

        self.translate(old_centroid[0], old_centroid[1])

    def rotate_point(self, angle, point):
        """
        rotates the polygon by degrees about a defined point
        """

        origin = (point[0], point[1])
        self.translate(-origin[0], -origin[1])

        for coord_i in range(self.__num_of_points):
            old_coord_x = self.__coord_list[coord_i][0]
            old_coord_y = self.__coord_list[coord_i][1]
            self.__coord_list[coord_i][0] = (cos(radians(angle)) * old_coord_x) - (sin(radians(angle)) * old_coord_y)
            self.__coord_list[coord_i][1] = (sin(radians(angle)) * old_coord_x) + (cos(radians(angle)) * old_coord_y)

        self.translate(origin[0], origin[1])
        self.__centroid = self.__cal_centroid()

    def get_area(self):
        """
        returns the area of the polygon as enclosed by it's vertices
        """

        last_index = self.__num_of_points - 1
        sum = 0
        for i in range(self.__num_of_points):
            if (i == last_index):
                sum += (self.__coord_list[i][0] * self.__coord_list[0][1]) - (self.__coord_list[i][1]*self.__coord_list[0][0])
            else:
                sum += (self.__coord_list[i][0] * self.__coord_list[i+1][1]) - (self.__coord_list[i][1] * self.__coord_list[i+1][0])

        return abs(sum/2)