import pygame
import numpy as np
from config import *
from Object3D import *
import copy


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

move_speed = 0.5
rotation_speed = 0.2
zoom_speed = 1

polygons_definitions = [
    ([0, 1, 2, 3], COLORS[0]),
    ([4, 5, 6, 7], COLORS[1]),
    ([0, 1, 5, 4], COLORS[2]),
    ([2, 3, 7, 6], COLORS[3]),
    ([0, 3, 7, 4], COLORS[4]),
    ([1, 2, 6, 5], COLORS[5]),
]

pointsA = []
pointsA.append(Point([0, 0, 0, 1]))
pointsA.append(Point([0, 1, 0, 1]))
pointsA.append(Point([1, 1, 0, 1]))
pointsA.append(Point([1, 0, 0, 1]))
pointsA.append(Point([0, 0, 1, 1]))
pointsA.append(Point([0, 1, 1, 1]))
pointsA.append(Point([1, 1, 1, 1]))
pointsA.append(Point([1, 0, 1, 1]))

polygonsA = []
for indices, color in polygons_definitions:
    polygonsA.append(Polygon([pointsA[i] for i in indices], COLORS[polygons_definitions.index((indices, color))]))
objectA = Object3D(pointsA, polygonsA)
objectA.translate(np.array([2, 0, 0]))

pointsB=copy.deepcopy(pointsA)
polygonsB = []
for indices, color in polygons_definitions:
    color_index = (polygons_definitions.index((indices, color)) + 1) % len(COLORS) 
    polygonsB.append(Polygon([pointsB[i] for i in indices], COLORS[color_index]))
objectB = Object3D(pointsB, polygonsB)
objectB.translate(np.array([0, 0, 2]))
objectB.scale(0.5, 1, 0.5)

pointsC=copy.deepcopy(pointsA)
polygonsC = []
for indices, color in polygons_definitions:
    color_index = (polygons_definitions.index((indices, color)) + 4) % len(COLORS)  
    polygonsC.append(Polygon([pointsC[i] for i in indices], COLORS[color_index]))
objectC = Object3D(pointsC, polygonsC)
objectC.scale(0.5, 0.5, 0.5)

all_points = []
all_polygons = []
all_points = objectA.points + objectB.points + objectC.points
all_polygons = objectA.polygons + objectB.polygons + objectC.polygons

camera = Camera(np.array([1, 1, -4, 1]))

scene = Object3D(all_points, all_polygons, camera=camera, screen=screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  
            camera.control(event)      

    screen.fill(pg.Color("darkslategray"))

    scene.draw()
    pygame.display.flip()

pygame.quit()
