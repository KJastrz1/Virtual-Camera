import math
import numpy as np


def projection_matrix(camera):
    NEAR = camera.near_plane
    FAR = camera.far_plane
    RIGHT = math.tan(camera.h_fov / 2)
    LEFT = -RIGHT
    TOP = math.tan(camera.v_fov / 2)
    BOTTOM = -TOP

    m00 = 2 / (RIGHT - LEFT)
    m11 = 2 / (TOP - BOTTOM)
    m22 = (FAR + NEAR) / (FAR - NEAR)
    m32 = -2 * NEAR * FAR / (FAR - NEAR)
    return np.array([
        [m00, 0, 0, 0],
        [0, m11, 0, 0],
        [0, 0, m22, 1],
        [0, 0, m32, 0]
    ])
    
def to_screen_matrix(screen_width, screen_height):
    HW, HH = screen_width / 2, screen_height / 2
    return np.array([
           [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])
    
