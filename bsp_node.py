from geometry import plane_equation
from polygon import Polygon


class BSPNode:
    def __init__(self, polygon: Polygon):
        self.polygon = polygon
        if len(polygon.points) >= 3:
            self.normal, self.D = plane_equation(
                polygon.points[0], polygon.points[1], polygon.points[2]
            )
        else:
            self.normal, self.D = None, None
        self.front = None
        self.back = None
