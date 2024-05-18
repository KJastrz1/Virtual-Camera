import pygame as pg
import numpy as np
from transformation_matrices import *
from config import *
from point import *
from polygon import *
from typing import List
from functools import cmp_to_key


def compute_centroid(points: List[Point]):
    sum_x = sum(point.position[0] for point in points)
    sum_y = sum(point.position[1] for point in points)
    sum_z = sum(point.position[2] for point in points)
    num_points = len(points)
    return np.array([sum_x / num_points, sum_y / num_points, sum_z / num_points])


def normal_vector(point1: Point, point2: Point, point3: Point):
    v1 = np.array(point2.position[:3]) - np.array(point1.position[:3])
    v2 = np.array(point3.position[:3]) - np.array(point1.position[:3])
    normal = np.cross(v1, v2)
    return normal / np.linalg.norm(normal)


def plane_equation(point1: Point, point2: Point, point3: Point):
    normal = normal_vector(point1, point2, point3)
    D = -np.dot(normal, np.array(point1.position[:3]))
    return normal, D


def all_vertices_one_side(points: List[Point], normal, D):
    equation_val = [np.dot(normal, point.position[:3]) + D for point in points]
    camera_val = D
    for val in equation_val:
        if np.sign(val) != np.sign(camera_val):
            if abs(val) < 10**-8:
                continue
            else:
                return False
    return True


def all_vertices_opposite_side(points: List[Point], normal, D):
    equation_val = [np.dot(normal, point.position[:3]) + D for point in points]
    camera_val = D
    for val in equation_val:
        if np.sign(val) == np.sign(camera_val):
            if abs(val) <10**-8:
                continue
            else:
                return False
    return True


class Object3D:
    def __init__(self, points: List[Point], polygons: List[Polygon]):
        self.points = points
        self.polygons = polygons
        self.camera_distance = 1000

    def compare_polygons(
        self, poly1: Polygon, poly2: Polygon, points: List[Point]
    ):
        vertices1 = [point for point in poly1.points]
        vertices2 = [point for point in poly2.points]

        centroid1 = compute_centroid(vertices1)
        centroid2 = compute_centroid(vertices2)

        normal2, D2 = plane_equation(vertices2[0], vertices2[1], vertices2[2])
        normal1, D1 = plane_equation(vertices1[0], vertices1[1], vertices1[2])

        all_on_camera_side1 = all_vertices_one_side(vertices1, normal2, D2)
        all_on_camera_side2 = all_vertices_one_side(vertices2, normal1, D1)

        all_on_opposite_side1 = all_vertices_opposite_side(vertices1, normal2, D2)
        all_on_opposite_side2 = all_vertices_opposite_side(vertices2, normal1, D1)

        distance1 = centroid1[2]
        distance2 = centroid2[2]
        # if all_on_camera_side1 and all_on_opposite_side2:
        #     return -1
        # elif all_on_camera_side2 and all_on_opposite_side1 :
        #     return 1
        

        # if distance1 < distance2:
        #     return -1
        # elif distance1 > distance2:
        #     return 1
        # else:
        distance1 = np.sqrt(np.sum(centroid1**2))
        distance2 = np.sqrt(np.sum(centroid2**2))
        if distance1 < distance2:
            return -1
        elif distance1 > distance2:
            return 1
        else:
            return 0

    def sort_polygons(self, points: List[Point]):
        sorted_polygons = sorted(
            self.polygons,
            key=cmp_to_key(
                lambda p1, p2: self.compare_polygons(p1, p2, points)
            ),
            reverse=True,
        )
        return sorted_polygons

    def draw(self, screen):
        projected_points = {
            point: point.project_point(self.camera_distance) for point in self.points
        }
        sorted_polygons = self.sort_polygons(self.points)

        for polygon in sorted_polygons:
            points_to_draw = [projected_points[point].position for point in polygon.points]
            points_to_draw = [(point[0], point[1]) for point in points_to_draw]
            pg.draw.polygon(
                screen,
                polygon.color,
                points_to_draw,
            )

    def translate(self, vector):
        matrix = translation_matrix(vector)
        for point in self.points:
            point.position = np.dot(point.position, matrix)

    def rotate_x(self, angle):
        matrix = rotation_x_matrix(angle)
        for point in self.points:
            point.position = np.dot(point.position, matrix)

    def rotate_y(self, angle):
        matrix = rotation_y_matrix(angle)
        for point in self.points:
            point.position = np.dot(point.position, matrix)

    def rotate_z(self, angle):
        matrix = rotation_z_matrix(angle)
        for point in self.points:
            point.position = np.dot(point.position, matrix)

    def scale(self, x, y, z):
        matrix = scaling_matrix(x, y, z)
        for point in self.points:
            point.position = np.dot(point.position, matrix)

    def zoom(self, value):
        if self.camera_distance + value > 500 and self.camera_distance + value < 1200:
            self.camera_distance += value
