import pygame as pg
import numpy as np
from transformation_matrices import *
from config import *
from point import *
from polygon import *
from typing import List
from bsp_node import *
from camera import *
from projection import *


def classify_vertex(vertex, plane_normal, plane_d):
    distance = np.dot(vertex[:3], plane_normal) + plane_d
    if np.isclose(distance, 0, atol=1e-5):
        return 0
    elif distance < 0:
        return -1
    else:
        return 1


def intersect_point(p1, p2, plane_normal, plane_d):
    d1 = np.dot(p1[:3], plane_normal) + plane_d  
    d2 = np.dot(p2[:3], plane_normal) + plane_d 
    t = -d1 / (d2 - d1)
    point_position=p1 + t * (p2 - p1)
    return np.append(point_position, 1)


def classify_polygon(polygon, plane_normal, plane_d):
    front = []
    back = []
    points = polygon.points

    vertex_class = [
        classify_vertex(pt.position, plane_normal, plane_d) for pt in points
    ]

    if all(v >= 0 for v in vertex_class):
        front.append(polygon)
    elif all(v <= 0 for v in vertex_class):
        back.append(polygon)
    else:
        print("Splitting polygon")
        front_points = []
        back_points = []
        num_vertices = len(points)

        for i in range(num_vertices):
            current_point = points[i]
            next_point = points[(i + 1) % num_vertices]
            current_class = vertex_class[i]
            next_class = vertex_class[(i + 1) % num_vertices]

            if current_class >= 0:
                front_points.append(current_point)
            if current_class <= 0:
                back_points.append(current_point)

            if current_class * next_class < 0:
                intersect = intersect_point(
                    current_point.position[:3], next_point.position[:3], plane_normal, plane_d
                )        
                inter_point = Point(intersect)
                inter_point.project
                front_points.append(inter_point)
                back_points.append(inter_point)

        if len(set((pt.position[0], pt.position[1]) for pt in front_points)) >= 3:            
            front.append(Polygon(front_points, polygon.color))
        if len(set((pt.position[0], pt.position[1]) for pt in back_points)) >= 3:
            back.append(Polygon(back_points, polygon.color))

    return front, back


def build_bsp_tree(polygons):
    if not polygons:
        return None

    node = BSPNode(polygons.pop(0))
    front_polygons = []
    back_polygons = []

    plane_normal, plane_d = plane_equation(
        node.polygon.points[0], node.polygon.points[1], node.polygon.points[2]
    )

    for poly in polygons:
        front, back = classify_polygon(poly, plane_normal, plane_d)
        front_polygons.extend(front)
        back_polygons.extend(back)

    node.front = build_bsp_tree(front_polygons)
    node.back = build_bsp_tree(back_polygons)

    return node


class Object3D:
    def __init__(
        self,
        points: List[Point],
        polygons: List[Polygon],
        camera: Camera = None,
        screen=None,
    ):
        self.points = points
        self.polygons = polygons
        self.camera = camera
        self.screen = screen
        self.tree_head: BSPNode = None

    def render_bsp_tree(self, node: BSPNode):
        if node is None:
            return
        
        camera_side = np.dot(self.camera.position[:3], node.normal) + node.D
        if camera_side < 0:
            self.render_bsp_tree(node.front)
            for point in node.polygon.points:
                point.project(self.camera)
            points_to_draw = [
                point.projected_position
                for point in node.polygon.points
                if point.visible
            ]
            if len(points_to_draw) > 2:
                pg.draw.polygon(self.screen, node.polygon.color, points_to_draw)
            self.render_bsp_tree(node.back)
        else:
            self.render_bsp_tree(node.back)
            for point in node.polygon.points:
                point.project(self.camera)
            points_to_draw = [
                point.projected_position
                for point in node.polygon.points
                if point.visible 
            ]  
            if len(points_to_draw) > 2:
                pg.draw.polygon(self.screen, node.polygon.color, points_to_draw)
            self.render_bsp_tree(node.front)

    def print_tree(self, node: BSPNode):
        if node is None:
            return
        self.print_tree(node.back)
        print(node.polygon.points)
        self.print_tree(node.front)

    def draw(self):
        if self.tree_head == None:
            self.tree_head = build_bsp_tree(self.polygons)

        self.render_bsp_tree(self.tree_head)

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
