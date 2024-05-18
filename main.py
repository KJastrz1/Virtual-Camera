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
    polygonsA.append(Polygon([pointsA[i] for i in indices], color))

objectA = Object3D(pointsA, polygonsA)
objectA.translate(np.array([2, 0, 10]))

objectB = copy.deepcopy(objectA)
objectB.translate(np.array([0, 0, 12]))
objectB.scale(0.5, 1, 0.5)

objectC = copy.deepcopy(objectA)
objectC.translate(np.array([0, 1, 10]))
objectC.scale(0.5, 0.5, 0.5)

all_points = [] 
all_polygons = []
all_points = objectA.points + objectB.points + objectC.points
all_polygons = objectA.polygons + objectB.polygons + objectC.polygons
scene=Object3D(all_points, all_polygons)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = pg.key.get_pressed()
            shift_pressed = key[pg.K_LSHIFT] or key[pg.K_RSHIFT]

            if shift_pressed:
                # Rotations with Shift
                if key[pg.K_a]:
                    scene.rotate_y(rotation_speed)
                if key[pg.K_d]:
                    scene.rotate_y(-rotation_speed)
                if key[pg.K_w]:
                    scene.rotate_x(rotation_speed)
                if key[pg.K_s]:
                    scene.rotate_x(-rotation_speed)
                if key[pg.K_q]:
                    scene.rotate_z(-rotation_speed)
                if key[pg.K_e]:
                    scene.rotate_z(rotation_speed)
            else:
                if key[pg.K_q]:
                    scene.rotate_z(rotation_speed)
                if key[pg.K_e]:
                    scene.rotate_z(-rotation_speed)
                # Movement without Shift
                if key[pg.K_a]:
                    scene.translate(np.array([1, 0, 0]) * move_speed)
                if key[pg.K_d]:
                    scene.translate(np.array([-1, 0, 0]) * move_speed)
                if key[pg.K_w]:
                    scene.translate(np.array([0, 1, 0]) * move_speed)
                if key[pg.K_s]:
                    scene.translate(np.array([0, -1, 0]) * move_speed)
                if key[pg.K_UP]:
                    scene.translate(np.array([0, 0, -1]) * move_speed)
                if key[pg.K_DOWN]:
                    scene.translate(np.array([0, 0, 1]) * move_speed)
                if key[pg.K_z]:
                    scene.zoom(-zoom_speed)
                if key[pg.K_x]:
                    scene.zoom(zoom_speed)


    screen.fill(pg.Color("darkslategray"))

    scene.draw(screen)
    pygame.display.flip()

pygame.quit()
