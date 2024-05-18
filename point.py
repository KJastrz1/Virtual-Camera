import numpy as np
from config import *

class Point:
    def __init__(self, position):
       self.position=np.array(position)
       
       
    def project_point(self, camera_distance):
        x = SCREEN_HEIGHT / 2 + camera_distance * self.position[0] / self.position[2]
        y = SCREEN_WIDTH / 2 + camera_distance * self.position[1] / self.position[2]
        return Point([x, y, self.position[2], 1])