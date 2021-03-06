import numpy as np
import pygame
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from math3D import *

# Global settings
# Screen stuff
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_HEIGHT = SCREEN_HEIGHT // 2
# Colors
BG_COLOR = (0, 0, 0)
OBJECT_COLOR = (255, 255, 255)
# Interface
FPS = 60
ANGLE_FACTOR = 100
mode = 'x'
rotating = False
side = 1

# pygame initialization
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
dt = 0
# Screen settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('[1.3] Leyba Rusakov Urban')
# Font for text rendering
font = pygame.font.SysFont('Courier New', 15)

# Object and rotation point declaration
A = 200
HF_A = A / 2
cube = np.array([
        [-HF_A, HF_A, HF_A, 1], 
        [-HF_A, -HF_A, HF_A, 1], 
        [HF_A, -HF_A, HF_A, 1], 
        [HF_A, HF_A, HF_A, 1], 
        [-HF_A, HF_A, -HF_A, 1], 
        [-HF_A, -HF_A, -HF_A, 1], 
        [HF_A, -HF_A, -HF_A, 1], 
        [HF_A, HF_A, -HF_A, 1], 
    ])
projected_cube = None
# Rotation angle (rad)
alpha = -np.pi / 60
beta = np.pi / 100
gamma = -np.pi / 60
angles = dict(zip('xyz', [alpha, beta, gamma]))


def fill_background():
    screen.fill(BG_COLOR)


def draw_square(a, b, c, d, color=OBJECT_COLOR):
    pygame.draw.line(screen, color, a, b)
    pygame.draw.line(screen, color, b, c)
    pygame.draw.line(screen, color, c, d)
    pygame.draw.line(screen, color, d, a)


def draw_cube(object, color=OBJECT_COLOR):
    draw_square(*[object[i, :2] for i in range(4)])
    draw_square(*[object[i, :2] for i in range(4, 8)])
    draw_square(object[0, :2], object[4, :2], object[5, :2], object[1, :2])
    draw_square(object[2, :2], object[6, :2], object[7, :2], object[3, :2])
    pygame.draw.circle(screen, (255, 0, 0), object[1, :2], 5)
    pygame.draw.circle(screen, (255, 0, 0), object[-1, :2], 5)


def draw_pyramid(object, color=OBJECT_COLOR):
    draw_square(*[object[i, :2] for i in range(4)])
    for p in object[:4, :2]:
        pygame.draw.line(screen, color, object[-1, :2], p)


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


projected_cube = project_isometric(cube)
projected_cube = translate(projected_cube, [HALF_WIDTH, HALF_HEIGHT, 0, 0])
# projected_pyramid = project_isometric(pyramid)
# projected_pyramid = translate(projected_pyramid, [HALF_WIDTH, HALF_HEIGHT, 0, 0])
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
        cube = rotate(cube, 'xyz', (sign * angles['x'], sign * angles['y'], sign * angles['z']))
        projected_cube = project_isometric(cube)
        projected_cube = translate(projected_cube, [HALF_WIDTH, HALF_HEIGHT, 0, 0])

    # Clear screen
    fill_background()
    # Draw geometry
    draw_cube(projected_cube)
    draw_text()


    # Update screen
    pygame.display.update()
    dt = clock.tick(60)