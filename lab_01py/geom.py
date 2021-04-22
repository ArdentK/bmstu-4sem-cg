from math import sqrt, pi


def triangle_area(p1, p2, p3):
    return abs((p1[0] - p3[0])*(p2[1]-p3[1])-(p2[0]-p3[0])*(p1[1]-p3[1]))/2


def circle_area(radius):
    return pi * radius**2


def point_dist(p1, p2):
    return sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))


def correct_triangle(p1, p2, p3):
    if point_dist(p1, p2) + point_dist(p1, p3) <= point_dist(p2, p3):
        return False
    if point_dist(p1, p3) + point_dist(p2, p3) <= point_dist(p1, p2):
        return False
    if point_dist(p1, p2) + point_dist(p2, p3) <= point_dist(p1, p3):
        return False

    return True


def get_circle_center(p1, p2, p3):

    begin1, end1, begin2, end2 = get_perpendicular_bisector(
        p1, p2, p3)

    a1 = begin1[1] - end1[1]
    b1 = end1[0] - begin1[0]
    c1 = begin1[0] * end1[1] - end1[0] * begin1[1]

    a2 = begin2[1] - end2[1]
    b2 = end2[0] - begin2[0]
    c2 = begin2[0] * end2[1] - end2[0] * begin2[1]

    det = a1 * b2 - a2 * b1

    x_center = (b1 * c2 - b2 * c1) / det
    y_center = (a2 * c1 - a1 * c2) / det

    return [x_center, y_center]


def get_solution(dots):

    solution = dict()
    solution["ind_p1"] = 0
    solution["ind_p2"] = 1
    solution["ind_p3"] = 2
    solution["center"] = -1.0
    solution["radius"] = -1.0
    solution["triangle_area"] = -1.0
    solution["circle_area"] = -1.0
    solution["difference"] = -1

    if (correct_triangle(dots[0], dots[1], dots[2])):
        solution["center"] = get_circle_center(dots[0], dots[1], dots[2])
        solution["radius"] = point_dist(dots[0], solution["center"])
        solution["triangle_area"] = triangle_area(dots[0], dots[1], dots[2])
        solution["circle_area"] = circle_area(solution["radius"])
        solution["difference"] = abs(
            solution["circle_area"] - solution["triangle_area"])

    for i in range(len(dots)):
        for j in range(i + 1, len(dots)-1):
            for k in range(j + 1, len(dots)-2):
                point_1 = dots[i]
                point_2 = dots[j]
                point_3 = dots[k]

                if (correct_triangle(point_1, point_2, point_3) == True):
                    center = get_circle_center(point_1, point_2, point_3)

                    radius = point_dist(center, point_1)

                    circle = circle_area(radius)
                    triangle = triangle_area(point_1, point_2, point_3)

                    if (abs(circle - triangle) > solution["difference"]):
                        solution["circle_area"] = circle
                        solution["triangle_area"] = triangle
                        solution["radius"] = radius
                        solution["center"] = center
                        solution["ind_p1"] = i
                        solution["ind_p2"] = j
                        solution["ind_p3"] = k
                        solution["difference"] = abs(circle - triangle)

    return solution


def get_perpendicular_bisector(p1, p2, p3, r1=-1, r2=-1):
    vector1 = [p2[1] - p1[1], p1[0] - p2[0]]

    begin1 = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]

    vector2 = [p3[1] - p1[1], p1[0] - p3[0]]

    begin2 = [(p1[0] + p3[0]) / 2, (p1[1] + p3[1]) / 2]

    end1 = [begin1[0] + vector1[0], begin1[1] + vector1[1]]

    end2 = [begin2[0] + vector2[0], begin2[1] + vector2[1]]

    begin1 = [begin1[0], begin1[1]]

    begin2 = [begin2[0], begin2[1]]

    return begin1, end1, begin2, end2
