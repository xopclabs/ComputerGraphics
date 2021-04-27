import numpy as np
import pygame
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figures import *


# Global settings
# Screen stuff
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_HEIGHT = SCREEN_HEIGHT // 2
AR = SCREEN_WIDTH / SCREEN_HEIGHT
FOV = 75
FAR = 1000
NEAR = 0.1
# Colors
BG_COLOR = (0, 0, 0)
OBJECT_COLOR = (255, 255, 255)
# Interface
FPS = 60
ANGLE_FACTOR = 100
mode = 'x'
rotating = False
sign = 1

# pygame initialization
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
dt = 0
# Screen settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('[5] Leyba Rusakov Urban')
# Font for text rendering
font = pygame.font.SysFont('Courier New', 15)

# Object declaration
OFFSET = 5
object = Object(obj_to_coords('lab5/models/cube.obj')).rotateX(3*np.pi/2).rotateY(13*np.pi/12)
projected_object = object.translate([0, 0, OFFSET], copy=True).project(AR, FOV, FAR, NEAR)
wireframe = False

# Rotation angle (rad)
alpha = 0
beta = np.pi / 100
gamma = 0
angles = dict(zip('xyz', [alpha, beta, gamma]))


def fill_background():
    screen.fill(BG_COLOR)


def draw_text():
    str = [
        f'α = {angles["x"] / np.pi * FPS: .2f}π / s (x-axis)', 
        f'β = {angles["y"] / np.pi * FPS: .2f}π / s (y-axis)', 
        f'γ = {angles["z"] / np.pi * FPS: .2f}π / s (z-axis)'
    ]
    for i, s in enumerate(str):
        color = (175, 175, 175) if s[-7] != mode else (255, 255, 255)
        text_surface = font.render(s, False, color)
        screen.blit(text_surface, (5, i * 14 + 1))


# Main loop
while True:
    # Event handling
    for event in pygame.event.get():
        # Quitting
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Set R to reset cube
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                mode = 'x'
            if event.key == pygame.K_y:
                mode = 'y'
            if event.key == pygame.K_z:
                mode = 'z'
            if event.key == pygame.K_w:
                wireframe = not wireframe
            if event.key == pygame.K_r:
                angles[mode] = 0
        # On mouse scroll, change angle
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse Wheel Up
            if event.button == 4:
                angles[mode] += np.pi / ANGLE_FACTOR * dt / FPS
                angles[mode] = angles[mode] if angles[mode] < 2 * np.pi else 2 * np.pi
            # Mouse Wheel Down
            if event.button == 5:
                angles[mode] -= np.pi / ANGLE_FACTOR * dt / FPS
                angles[mode] = angles[mode] if angles[mode] > -2 * np.pi else -2 * np.pi
            # LMB
            if event.button == 1:
                rotating = True
                sign = 1
            # RMB
            if event.button == 3:
                rotating = True
                sign = -1
        if event.type == pygame.MOUSEBUTTONUP:
            # LMB
            if event.button == 1:
                rotating = False
                sign = 1
            # RMB
            if event.button == 3:
                rotating = False
                sign = -1

    if rotating:
        object = object.rotateX(sign * angles['x']).rotateY(sign * angles['y']).rotateZ(sign * angles['z'])
        projected_object = object.translate([0, 0, OFFSET], copy=True).project(AR, FOV, FAR, NEAR)

    # Clear screen
    fill_background()
    # Draw geometry
    projected_object.prepare(screen, copy=True).draw(screen, wireframe=wireframe)
    draw_text()

    # Update screen
    pygame.display.update()
    dt = clock.tick(60)

