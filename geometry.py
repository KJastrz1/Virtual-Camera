from point import Point
import numpy as np

def normal_vector(point1: Point, point2: Point, point3: Point):
    v1 = np.array(point2.position[:3]) - np.array(point1.position[:3])
    v2 = np.array(point3.position[:3]) - np.array(point1.position[:3])
    normal = np.cross(v1, v2)
    return normal / np.linalg.norm(normal)


def plane_equation(point1: Point, point2: Point, point3: Point):
    normal = normal_vector(point1, point2, point3)
    D = -np.dot(normal, np.array(point1.position[:3]))
    return normal, D