import numpy as np
from config import *

class Point:
    def __init__(self, position):
       self.position=np.array(position)
       self.projected_position=None
       
       
