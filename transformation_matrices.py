import math 
import numpy as np


def translation_matrix(vector):
    tx, ty, tz = vector
    return np.array([
    [1, 0, 0, tx],
    [0, 1, 0, ty],
    [0, 0, 1, tz],
    [0, 0, 0, 1]
    ]).T
    
def rotation_x_matrix(angle):
    cos = math.cos(angle)
    sin = math.sin(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, cos, -sin, 0],
        [0, sin, cos, 0],
        [0, 0, 0, 1]
    ]).T
    
def rotation_y_matrix(angle):
    cos = math.cos(angle)
    sin = math.sin(angle)
    return np.array([
        [cos, 0, sin, 0],
        [0, 1, 0, 0],
        [-sin, 0, cos, 0],
        [0, 0, 0, 1]
    ]).T

def rotation_z_matrix(angle):
    cos = math.cos(angle)
    sin = math.sin(angle)
    return np.array([
        [cos, -sin, 0, 0],
        [sin, cos, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]).T
    
def scaling_matrix(x,y,z):
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ]).T
    
    