import numpy as np
import pygame
from copy import deepcopy, copy
from obj_reader import obj_to_coords
from math3D import *


class Object():
    def __init__(self, polygons, normals=None):
        self.polygons = polygons.astype(np.float32)
        self.center = self.polygons.mean(axis=0).mean(axis=0).reshape(1, 4)
        self.normals = normals
        if self.normals is None:
            self.normals = get_normal(self.polygons)
        self._update_visibility()


    def _update_visibility(self):
        self.visibility = np.sum(self.normals * self.polygons[:, 0, :], axis=-1) - 1 < 0


    def translate(self, delta, copy=False):
        obj = deepcopy(self) if copy else self
        obj.polygons = translate(obj.polygons, delta)
        obj.center = translate(obj.center, delta)
        return obj 


    def rotateX(self, angle, copy=False, with_normals=True):
        obj = deepcopy(self) if copy else self
        obj.polygons = rotateX(obj.polygons, angle)
        obj.center = rotateX(obj.center, angle)
        if with_normals:
            obj.normals = rotateX(obj.normals, angle)
            obj.normals = normalize(obj.normals)
        return obj 
    

    def rotateY(self, angle, copy=False, with_normals=True):
        obj = deepcopy(self) if copy else self
        obj.polygons = rotateY(obj.polygons, angle)
        obj.center = rotateY(obj.center, angle)
        if with_normals:
            obj.normals = rotateY(obj.normals, angle)
            obj.normals = normalize(obj.normals)
        return obj 
    

    def rotateZ(self, angle, copy=False, with_normals=True):
        obj = deepcopy(self) if copy else self
        obj.polygons = rotateZ(obj.polygons, angle)
        obj.center = rotateZ(obj.center, angle)
        if with_normals:
            obj.normals = rotateZ(obj.normals, angle)
            obj.normals = normalize(obj.normals)
        return obj 


    def scale(self, s, copy=False):
        obj = deepcopy(self) if copy else self
        obj.polygons = scale(obj.polygons, s)
        obj.center = scale(obj.center, s)
        return obj 


    def project(self, aspectratio, fov, far, near, copy=False):
        obj = deepcopy(self) if copy else self
        obj.polygons = project(obj.polygons, aspectratio, fov, far, near)
        obj.center = project(obj.center, aspectratio, fov, far, near)
        return obj


    def prepare(self, screen, copy=False):
        w, h = screen.get_size()
        obj = deepcopy(self) if copy else self
        obj.translate([1, 1, 0]).scale([0.5 * w, 0.5 * h, 1])
        return obj


    def draw(self, screen):
        self.normals = get_normal(self.polygons)
        self._update_visibility()
        pygame.draw.circle(screen, (255, 0, 0), self.center[0, :2], 2)
        for p, visible in zip(self.polygons, self.visibility):
            if visible:
                pygame.draw.line(screen, (255, 255, 255), p[0, :2], p[1, :2])
                pygame.draw.line(screen, (255, 255, 255), p[1, :2], p[2, :2])
                pygame.draw.line(screen, (255, 255, 255), p[2, :2], p[0, :2])


class Box(Object):
    def __init__(self, pos, size):
        x, y, z = size
        self.polygons = np.array([
            [[0, 0, 0, 1], [0, y, 0, 1], [x, y, 0, 1]],
            [[0, 0, 0, 1], [x, y, 0, 1], [x, 0, 0, 1]],
            [[x, 0, 0, 1], [x, y, 0, 1], [x, y, z, 1]],
            [[x, 0, 0, 1], [x, y, z, 1], [x, 0, z, 1]],
            [[x, 0, z, 1], [x, y, z, 1], [0, y, z, 1]],
            [[x, 0, z, 1], [0, y, z, 1], [0, 0, z, 1]],
            [[0, 0, z, 1], [0, y, z, 1], [0, y, 0, 1]],
            [[0, 0, z, 1], [0, y, 0, 1], [0, 0, 0, 1]],
            [[0, y, 0, 1], [0, y, z, 1], [x, y, z, 1]],
            [[0, y, 0, 1], [x, y, z, 1], [x, y, 0, 1]],
            [[x, 0, z, 1], [0, 0, z, 1], [0, 0, 0, 1]],
            [[x, 0, z, 1], [0, 0, 0, 1], [x, 0, 0, 1]]
        ])
        super(Box, self).__init__(self.polygons)
        self.translate(pos)
