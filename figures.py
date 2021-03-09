import numpy as np
import pygame
from copy import deepcopy, copy
from polygon import Polygon
from obj_reader import obj_to_coords


class Object():
    def draw(self, screen, prepare=False):
        for p in self.polygons:
            p.draw(screen, prepare)


    def prepare(self, screen, copy=False):
        x, y = screen.get_size()
        obj = deepcopy(self) if copy else self
        for p in obj.polygons:
            p.prepare(x, y)
        return obj


    def rotateX(self, angle, copy=False):
        obj = deepcopy(self) if copy else self
        for p in obj.polygons:
            p.rotateX(angle)
        return obj 
    

    def rotateY(self, angle, copy=False):
        obj = deepcopy(self) if copy else self
        for p in obj.polygons:
            p.rotateY(angle)
        return obj 
    

    def rotateZ(self, angle, copy=False):
        obj = deepcopy(self) if copy else self
        for p in obj.polygons:
            p.rotateZ(angle)
        return obj


    def translate(self, delta, copy=False):
        obj = deepcopy(self) if copy else self
        for p in obj.polygons:
            p.translate(delta)
        return obj


    def scale(self, scale, copy=False):
        obj = deepcopy(self) if copy else self
        for p in obj.polygons:
            p.scale(scale)
        return obj


    def project(self, aspectratio, fov, far, near, copy=False):
        obj = deepcopy(self) if copy else self
        for p in obj.polygons:
            p.project(aspectratio, fov, far, near)
        return obj



class Box(Object):
    def __init__(self, pos, size, color=None):
        self.size = size
        if color is None:
            self.color = [(255, 255, 255) for _ in range(12)]
        elif len(color) == 6:
            self.color = [c for c in color for _ in range(2)]
        else:
            self.color = color
        x, y, z = self.size
        self.polygons = [
            # Rear
            Polygon([0, 0, 0], [0, y, 0], [x, y, 0], self.color[0]),
            Polygon([x, y, 0], [x, 0, 0], [0, 0, 0], self.color[1]),
            # Front
            Polygon([0, 0, z], [0, y, z], [x, y, z], self.color[2]),
            Polygon([x, y, z], [x, 0, z], [0, 0, z], self.color[3]),
            # Right
            Polygon([x, 0, 0], [x, y, 0], [x, y, z], self.color[4]),
            Polygon([x, y, z], [x, 0, z], [x, 0, 0], self.color[5]),
            # Left
            Polygon([0, 0, 0], [0, y, 0], [0, y, z], self.color[6]),
            Polygon([0, y, z], [0, 0, z], [0, 0, 0], self.color[7]),
            # Top
            Polygon([0, y, z], [0, y, 0], [x, y, 0], self.color[8]),
            Polygon([x, y, 0], [x, y, z], [0, y, z], self.color[9]),
            # Bottom
            Polygon([0, 0, z], [0, 0, 0], [x, 0, 0], self.color[10]),
            Polygon([x, 0, 0], [x, 0, z], [0, 0, z], self.color[11]),
        ]
        for i in range(12):
            self.polygons[i].m += np.hstack((np.array(pos), [0]))

    
    def __str__(self):
        string = ''
        ranges = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12)]
        sides = ['rear', 'front', 'right', 'left', 'top', 'bottom']
        for r, side in zip(ranges, sides):
            l = ', '.join([str(p) for p in self.polygons[r[0]:r[1]]])
            string += f'{side:6s}: [{l}]\n'
        return string.strip()

    
class Sphere(Object):
    def __init__(self, model_path, color=(255, 255, 255)):
        coords = obj_to_coords(model_path)
        self.polygons = [Polygon(*x, color) for x in coords]
        self.color = color


    def __str__(self):
        string = ''
        ranges = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12)]
        for r in ranges:
            l = ', '.join([str(p) for p in self.polygons[r[0]:r[1]]])
            string += f'[{l}]\n'
        return string.strip()
        