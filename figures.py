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
        print(self.colors)
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
        return obj


    def draw(self, screen):
        """
        w, h = depths.shape[0] - 1, depths.shape[1] - 1
        def draw_line(p0, p1):
            x0, y0, z0 = p0
            x1, y1, z1 = p1
            l = x1 - x0
            m = y1 - y0
            n = z1 - z0
            delta_err = np.abs(m / l)
            error = 0.0
            y = int(y0)
            for x in range(int(x0), int(x1)):
                x = 0 if x < 0 else x
                x = w if x > w else x
                y = 0 if y < 0 else y
                y = h if y > h else y

                z = z0 + (m * (x - x0) - l * (y - y0)) / n
                if z < depths[x, y]:
                    depths[x, y] = z
                    c = int(1e4 / (1 - z) * 255) + 25
                    c = 255 if c > 255 else c
                    pixels[x, y, :] = [c, c, c]
                error += delta_err
                if error >= 0.5:
                    y += int(m > 0)
                    error -= 1.0

        """
        self.normals = get_normal(self.polygons)
        self._update_visibility()
        for i, (p, visible) in enumerate(zip(self.polygons, self.visibility)):
            if visible:
               pygame.draw.line(screen, (self.colors[i], self.colors[i], self.colors[i]), p[0, :2], p[1, :2])
               pygame.draw.line(screen, (self.colors[i], self.colors[i], self.colors[i]), p[1, :2], p[2, :2])
               pygame.draw.line(screen, (self.colors[i], self.colors[i], self.colors[i]), p[2, :2], p[0, :2])


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
