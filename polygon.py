from point import *
from config import *
from typing import List

class Polygon:
    def __init__(self, points: List[Point],color):
        self.points = points
        self.color=color