import numpy as np
from config import *
from projection import *
from camera import *


class Point:
    def __init__(self, position):
        self.position = np.array(position)
        self.projected_position = None
        self.visible = True

    def project(self, camera: Camera):
        self.visible = True
        self.projected_position = np.dot(self.position, camera.view_matrix())
        if self.projected_position[2] < 0:
            self.visible = False
        self.projected_position = np.dot(
            self.projected_position, projection_matrix(camera)
        )
        self.projected_position = self.projected_position / self.projected_position[3]

        for i in range(2):
            if self.projected_position[i] > 3 or self.projected_position[i] < -3:
                self.visible = False

        self.projected_position = np.dot(
            self.projected_position, to_screen_matrix(SCREEN_WIDTH, SCREEN_HEIGHT)
        )[:2]
