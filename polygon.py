import numpy as np
import pygame
from copy import deepcopy
from collections.abc import Sequence


class Polygon:
    def __init__(self, a, b, c, normal=None, color=None):
        self.m = np.hstack((np.array([a, b, c], dtype=np.float32), np.ones((3, 1))))
        self.normal = normal
        if self.normal is None:
            self.update_normal()
        self.color = color if color is not None else (255, 255, 255)

    
    def __str__(self):
        return '[' + ', '.join([f'{x: .3f}' for x in self.m[0]]) + ']'


    def prepare(self, width, height, copy=False):
        p = deepcopy(self) if copy else self
        return p.translate([1, 1, 0]).scale([0.5 * width, 0.5 * height, 1])


    def draw(self, screen, prepare=False):
        if prepare:
            w, h = screen.get_size()
            p = self.prepare(w, h, True)
        else:
            p = self
        pygame.draw.line(screen, p.color, p.m[0, :2], p.m[1, :2])
        pygame.draw.line(screen, p.color, p.m[1, :2], p.m[2, :2])
        pygame.draw.line(screen, p.color, p.m[2, :2], p.m[0, :2])


    def update_normal(self):
        A = self.m[1] - self.m[0]
        B = self.m[2] - self.m[0]
        self.update_normal = np.array([
            A[1] * B[2] - A[2] * B[1],
            A[2] * B[0] - A[0] * B[2],
            A[0] * B[1] - A[1] * B[0]
        ])


    def rotateX(self, angle):
        # Rotates object around x axis
        T = np.array([
            [1, 0, 0, 0],
            [0, np.cos(angle), np.sin(angle), 0],
            [0, -np.sin(angle), np.cos(angle), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.m = self.m @ T
        return self

    def rotateY(self, angle):
        # Rotates object around y axis
        T = np.array([
            [np.cos(angle), 0, -np.sin(angle), 0],
            [0, 1, 0, 0],
            [np.sin(angle), 0, np.cos(angle), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.m = self.m @ T
        return self


    def rotateZ(self, angle):
        # Rotates object around z axis
        T = np.array([
            [np.cos(angle), np.sin(angle), 0, 0],
            [-np.sin(angle), np.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.m = self.m @ T
        return self


    def translate(self, delta):
        T = np.identity(4)
        T[3, :] = np.concatenate([np.array(delta), np.array([1])])
        self.m = self.m @ T
        return self


    def scale(self, scale):
        T = np.identity(4)
        if isinstance(scale, Sequence) and len(scale) == 3:
            np.fill_diagonal(T, np.concatenate([np.array(scale), np.array([1])]))
        else:
            T[3, 3] = 1 / scale
        self.m = self.m @ T
        h = self.m[:, 3, np.newaxis]
        h[h == 0] = 1
        self.m /= h
        return self

    def project(self, aspectratio, fov, far, near):
        fov_mult = 1 / np.tan(0.5 * fov * np.pi / 180)
        far_mult = far / (far - near)
        proj_matrix = np.array([
            [aspectratio * fov_mult, 0, 0, 0],
            [0, fov_mult, 0, 0],
            [0, 0, -far_mult, -1],
            [0, 0, -far_mult * near, 0]
        ], dtype=np.float32)
        self.m = self.m @ proj_matrix
        h = self.m[:, 3, np.newaxis]
        h[h == 0] = 1
        self.m /= h
        return self
