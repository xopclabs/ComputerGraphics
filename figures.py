import numpy as np
import pygame
from copy import deepcopy, copy
from itertools import chain
from obj_reader import obj_to_coords
from math3D import *


class Object():
    def __init__(self, polygons, normals=None):
        self.polygons = polygons.astype(np.float32)
        self.colors = np.linspace(50, 255, self.polygons.shape[0], dtype=np.uint8)
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


    def rotateX(self, angle, around=None, copy=False):
        obj = deepcopy(self) if copy else self
        if around == 'center':
            obj.polygons = rotateX(obj.polygons, angle, around=self.center[:3])
        else:
            obj.polygons = rotateX(obj.polygons, angle)
            obj.center = rotateX(obj.center, angle)
        return obj


    def rotateY(self, angle, around=None, copy=False):
        obj = deepcopy(self) if copy else self
        if around == 'center':
            obj.polygons = rotateY(obj.polygons, angle, around=self.center[:3])
        else:
            obj.polygons = rotateY(obj.polygons, angle)
            obj.center = rotateY(obj.center, angle)
        return obj


    def rotateZ(self, angle, around=None, copy=False):
        obj = deepcopy(self) if copy else self
        if around == 'center':
            obj.polygons = rotateZ(obj.polygons, angle, around=self.center[:3])
        else:
            obj.polygons = rotateZ(obj.polygons, angle)
            obj.center = rotateZ(obj.center, angle)
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
        z_means = obj.polygons.mean(axis=1)[:, 2]
        sort_idx = np.argsort(z_means)
        obj.polygons = obj.polygons[sort_idx]
        obj.colors = obj.colors[sort_idx]
        return obj


    def draw(self, screen, wireframe=True):
        self.normals = get_normal(self.polygons)
        self._update_visibility()
        for i, (p, visible) in enumerate(zip(self.polygons, self.visibility)):
            #if visible:
            if wireframe:
               pygame.draw.line(screen, (self.colors[i],)*3, p[0, :2], p[1, :2])
               pygame.draw.line(screen, (self.colors[i],)*3, p[1, :2], p[2, :2])
               pygame.draw.line(screen, (self.colors[i],)*3, p[2, :2], p[0, :2])
            else:
               pygame.draw.polygon(screen,  (self.colors[i],)*3, p[:, :2])


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


class BilinearPlane(Object):
    def __init__(self, points, n=1):
        self.points = np.array([p + [1] for p in points])
        self.polygons = self._generate_grid(n)
        super(BilinearPlane, self).__init__(self.polygons)
        for c_i in range(0, self.colors.size, 2):
            sq_i = c_i // 2
            i, j = sq_i % n, sq_i // n
            if i % 2 == j % 2:
                self.colors[c_i] = 255
                self.colors[c_i + 1] = 255
            else:
                self.colors[c_i] = 70
                self.colors[c_i + 1] = 70


    def _generate_grid(self, n):
        def get_square(i, j):
            s = 1 / n
            lb = self._point_by_equation(i*s, j*s)
            rb = self._point_by_equation(i*s + s, j*s)
            lt = self._point_by_equation(i*s, j*s + s)
            rt = self._point_by_equation(i*s + s, j*s + s)
            top = [lb, lt, rt]
            bot = [rt, rb, lb]
            return top, bot
        polygons = []
        for i in range(n):
            for j in range(n):
                top, bot = get_square(i, j)
                polygons.append(top)
                polygons.append(bot)
        return np.array(polygons)


    def _point_by_equation(self, u, w):
        p00, p01, p10, p11 = self.points
        return p00*(1 - u)*(1 - w) + p01*(1 - u)*w + p10*u*(1 - w) + p11*u*w


    def translate(self, delta, copy=False):
        obj = super(BilinearPlane, self).translate(delta, copy=copy)
        obj.points = translate(obj.points, delta)
        return obj


    def rotateX(self, angle, around=None, copy=False):
        obj = super(BilinearPlane, self).rotateX(angle, copy=copy)
        obj.points = rotateX(obj.points, angle)
        return obj


    def rotateY(self, angle, around=None, copy=False):
        obj = super(BilinearPlane, self).rotateY(angle, copy=copy)
        obj.points = rotateY(obj.points, angle)
        return obj


    def rotateZ(self, angle, around=None, copy=False):
        obj = super(BilinearPlane, self).rotateZ(angle, copy=copy)
        obj.points = rotateZ(obj.points, angle)
        return obj


    def scale(self, s, copy=False):
        obj = super(BilinearPlane, self).scale(s, copy=copy)
        obj.points = scale(obj.points, s)
        return obj


    def project(self, aspectratio, fov, far, near, copy=False):
        obj = super(BilinearPlane, self).project(aspectratio, fov, far, near, copy=copy)
        obj.points = project(obj.points, aspectratio, fov, far, near)
        return obj


    def prepare(self, screen, copy=False):
        obj = super(BilinearPlane, self).prepare(screen, copy=copy)
        w, h = screen.get_size()
        obj.points = translate(obj.points, [1, 1, 0])
        return obj


    def draw(self, screen, wireframe=False):
        super(BilinearPlane, self).draw(screen, wireframe=wireframe)
        for poly in self.polygons:
            for p in poly:
                pygame.draw.circle(screen, (255, 0, 0), p[:2], 2)

