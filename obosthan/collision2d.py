# Copyright (c) 2018-2019, Md Imam Hossain (emamhd at gmail dot com)
# see LICENSE.txt for details


"""
2d collision routines
"""

from .point2d import OPoint2D
from .vector2d import OVector2D


def ocircle2(circle1, circle1_radius, circle2, circle2_radius):
    """
    detects collision between two circles
    """

    if (circle1.distance_to(circle2) <= (circle1_radius+circle2_radius)):
        return True
    else:
        return False

def oline2(line1, line2):
    """
    detects collision between two definite lines and returns intersecting points
    """

    denominator = ((line1[2] - line1[0]) * (line2[3] - line2[1])) - ((line1[3] - line1[1]) * (line2[2] - line2[0]))
    numerator1 = ((line1[1] - line2[1]) * (line2[2] - line2[0])) - ((line1[0] - line2[0]) * (line2[3] - line2[1]))
    numerator2 = ((line1[1] - line2[1]) * (line1[2] - line1[0])) - ((line1[0] - line2[0]) * (line1[3] - line1[1]))

    if denominator == 0:
        return numerator1 == 0 and numerator2 == 0

    t = numerator1 / denominator

    u = numerator2 / denominator

    if (t >= 0 and t <= 1) and (u >= 0 and u <= 1):
        return OPoint2D(line1[0] + (t*(line1[2]-line1[0])), line1[1] + (t*(line1[3]-line1[1])))
    else:
        None

def oline_circle(line, circle, circle_radius):
    """
    detects collision between a line and a circle and returns penetration distance
    """

    origin_circle = OPoint2D(circle[0]-line[0], circle[1]-line[1])
    line_vector = OVector2D(0,0)
    circle_vector = OVector2D(0, 0)
    line_vector.define_line(line[0], line[1], line[2], line[3])
    circle_vector[0] = origin_circle[0]
    circle_vector[1] = origin_circle[1]
    circle_vector_project = line_vector.project(circle_vector)
    circle_project = OPoint2D(circle_vector_project[0], circle_vector_project[1])
    distance = circle_project.distance_to(origin_circle)
    if (distance < circle_radius):
        line_vector_end = OPoint2D(line_vector[0], line_vector[1])
        check_length = line_vector.length + circle_radius
        if (circle_vector_project.length < check_length and line_vector_end.distance_to(circle_project) < check_length):
            return circle_radius - distance
        else:
            return None
    else:
        return None

def obox2(poly1, poly2):
    """
    detects axis aligned collision between two polygons 
    """

    if len(poly1) != 0 and len(poly2) != 0:

        x_coords = []
        y_coords = []

        for coord_x, coord_y in poly1.coords:
            x_coords.append(coord_x)
            y_coords.append(coord_y)

        poly1_xcoord_min = min(x_coords)
        poly1_xcoord_max = max(x_coords)
        poly1_ycoord_min = min(y_coords)
        poly1_ycoord_max = max(y_coords)

        x_coords.clear()
        y_coords.clear()

        for coord_x, coord_y in poly2.coords:
            x_coords.append(coord_x)
            y_coords.append(coord_y)

        poly2_xcoord_min = min(x_coords)
        poly2_xcoord_max = max(x_coords)
        poly2_ycoord_min = min(y_coords)
        poly2_ycoord_max = max(y_coords)

        if poly1_xcoord_max >= poly2_xcoord_min and poly1_xcoord_min <= poly2_xcoord_max and poly1_ycoord_max >= poly2_ycoord_min and poly1_ycoord_min <= poly2_ycoord_max:
            return True
        else:
            return False
    else:
        return None

def obox_circle(poly, circle, circle_radius):
    """
    detects axis aligned collision between a polygon and circle 
    """

    if len(poly) != 0:

        x_coords = []
        y_coords = []

        for coord_x, coord_y in poly.coords:
            x_coords.append(coord_x)
            y_coords.append(coord_y)

        poly_xcoord_min = min(x_coords)
        poly_xcoord_max = max(x_coords)
        poly_ycoord_min = min(y_coords)
        poly_ycoord_max = max(y_coords)

        if (circle[0] + circle_radius) >= poly_xcoord_min and circle[0] <= (poly_xcoord_max + circle_radius) and (circle[1] + circle_radius) >= poly_ycoord_min and circle[1] <= (poly_ycoord_max + circle_radius):
            return True
        else:
            return False
    else:
        return None