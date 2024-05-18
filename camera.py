import numpy as np
from transformation_matrices import *
import math
from config import *
import pygame as pg


class Camera:
    def __init__(self, position):
        self.position = np.array(position, dtype=np.float64)
        self.forward = np.array([0, 0, 1, 1], dtype=np.float64)
        self.up = np.array([0, 1, 0, 1], dtype=np.float64)
        self.right = np.array([1, 0, 0, 1], dtype=np.float64)
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * SCREEN_HEIGHT / SCREEN_WIDTH
        self.near_plane = 0.1
        self.far_plane = 100
        self.angleX = 0
        self.angleY = -math.pi / 4
        self.angleZ = 0
        self.angles_changed = True
        self.position_changed = True
        self.move_speed = 0.5
        self.rotation_speed = math.pi / 12

    def control(self, event):
        if event.type != pg.KEYDOWN:
            return

        delta_angle = self.rotation_speed
        delta_pos = self.move_speed
        shift_pressed = (
            pg.key.get_pressed()[pg.K_LSHIFT] or pg.key.get_pressed()[pg.K_RSHIFT]
        )

        if shift_pressed:
            if event.key == pg.K_a:
                self.angleY -= delta_angle
            elif event.key == pg.K_d:
                self.angleY += delta_angle
            if event.key == pg.K_w:
                self.angleX -= delta_angle
            elif event.key == pg.K_s:
                self.angleX += delta_angle
            if event.key == pg.K_q:
                self.angleZ -= delta_angle
            elif event.key == pg.K_e:
                self.angleZ += delta_angle
            self.angles_changed = True
        else:
            if event.key == pg.K_a:
                self.position -= self.right * delta_pos
            elif event.key == pg.K_d:
                self.position += self.right * delta_pos
            if event.key == pg.K_w:
                self.position += self.up * delta_pos
            elif event.key == pg.K_s:
                self.position -= self.up * delta_pos
            if event.key == pg.K_UP:
                self.position += self.forward * delta_pos
            elif event.key == pg.K_DOWN:
                self.position -= self.forward * delta_pos
            self.position_changed = True

        if event.key == pg.K_z:
            self.zoom(-self.rotation_speed)
        elif event.key == pg.K_x:
            self.zoom(self.rotation_speed)

    def base_camera_vectors(self):
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axis(self):
        if self.angles_changed:           
            rotate_matrix = np.dot(
                rotation_x_matrix(self.angleX), rotation_z_matrix(self.angleZ)
            )
            rotate_matrix = np.dot(rotate_matrix, rotation_y_matrix(self.angleY))
            self.forward = np.dot(np.array([0, 0, 1, 1]), rotate_matrix)
            self.right = np.dot(np.array([1, 0, 0, 1]), rotate_matrix)
            self.up = np.dot(np.array([0, 1, 0, 1]), rotate_matrix)
            self.angles_changed = False

    def view_matrix(self):
        self.camera_update_axis()
        return np.dot(self.camera_translation_matrix(), self.camera_rotation_matrix())

    def zoom(self, zoom_speed):
        self.h_fov = max(min(self.h_fov + zoom_speed, math.pi / 2), math.pi / 6)
        self.v_fov = self.h_fov * SCREEN_HEIGHT / SCREEN_WIDTH

    def camera_translation_matrix(self):
        x, y, z, w = self.position
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-x, -y, -z, 1]])

    def camera_rotation_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up

        return np.array(
            [[rx, ux, fx, 0], [ry, uy, fy, 0], [rz, uz, fz, 0], [0, 0, 0, 1]]
        )
