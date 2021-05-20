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
LIGHT_STEP = 0.1
KEYS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_c, pygame.K_v, pygame.K_q, pygame.K_w]
ANGLE_FACTOR = 100
rotation_mode = [False, True, False]
rotating = False
sign = 1

# pygame initialization
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
dt = 0
# Screen settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('[6] Leyba Rusakov Urban')
# Font for text rendering
font = pygame.font.SysFont('Courier New', 10)

# Lighting setting
light_control_holds = [False] * 8
light_changed = False
light = np.array([1, 0, -1, 1], dtype=np.float32)
intensity = 1.0

# Object declaration
OFFSET = 15
object = Object(obj_to_coords('models/sphere.obj')).rotateX(3*np.pi/2).rotateY(13*np.pi/12)
projected_object = object.translate([0, 0, OFFSET], copy=True).illuminate(light, intensity=intensity).project(AR, FOV, FAR, NEAR)

wireframe = False

# Rotation angle (rad)
alpha = 0
beta = np.pi / 100
gamma = 0
angles = [alpha, beta, gamma]


def fill_background():
    screen.fill(BG_COLOR)


def draw_text():
    str = [
        f'α = {angles[0] / np.pi * FPS: .2f}π / s (x-axis)',
        f'β = {angles[1] / np.pi * FPS: .2f}π / s (y-axis)',
        f'γ = {angles[2] / np.pi * FPS: .2f}π / s (z-axis)'
    ]
    for i, s in enumerate(str):
        color = (150, 150, 150) if not rotation_mode[i] else (255, 255, 255)
        text_surface = font.render(s, False, color)
        screen.blit(text_surface, (5, i * 10 + 1))
    light_surface = font.render(f'Light: [{light[0]: .2f}, {light[1]: .2f}, {light[2]: .2f}]', False, (255, 255, 255))
    screen.blit(light_surface, (470, 1))
    intensity_surface = font.render(f'Intensity: {intensity*100: .2f}%', False, (255, 255, 255))
    screen.blit(intensity_surface, (521, 11))


def handle_light_control():
    global intensity
    for i, moving in enumerate(light_control_holds):
        if not moving:
            continue
        if i < 6:
            # Getting id for x, y, z coord in lighting vector
            # 0, 1 -> x, 2, 3 -> y etc.
            coord_i = i // 2
            # Choosing direction
            dir_sign = 1 if i % 2 == 0 else -1
            # Flipping direction for z
            if coord_i == 2:
                dir_sign *= -1
            # Moving the light "source"
            light[coord_i] += dir_sign * LIGHT_STEP * dt / FPS
        else:
            dir_sign = -1 if i % 2 == 0 else 1
            intensity += dir_sign * 0.05 * dt / FPS
            if intensity < 0:
                intensity = 0
            if intensity > 1:
                intensity = 1


# Main loop
while True:
    # Event handling
    for event in pygame.event.get():
        # Quitting
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Rotation toggles
            for i, key in enumerate([pygame.K_x, pygame.K_y, pygame.K_z]):
                if event.key == key:
                    rotation_mode[i] = not rotation_mode[i]
            # Rotation reset
            if event.key == pygame.K_r:
                for i in range(len(angles)):
                    angles[i] = 0
                rotaion_mode = [False, True, False]
            # Wireframe toggle
            if event.key == pygame.K_d:
                wireframe = not wireframe
            # Light source movement and intensity adjustments
            for i, key in enumerate(KEYS):
                if event.key == key:
                    light_control_holds[i] = True
                    light_changed = True
        if event.type == pygame.KEYUP:
            for i, key in enumerate(KEYS):
                if event.key == key:
                    light_control_holds[i] = False
        # On mouse scroll, change angle
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse Wheel Up
            if event.button == 4:
                for i in range(len(angles)):
                    if rotation_mode[i]:
                        angles[i] += np.pi / ANGLE_FACTOR * dt / FPS
                        angles[i] = angles[i] if angles[i] < 2 * np.pi else 2 * np.pi
            # Mouse Wheel Down
            if event.button == 5:
                for i in range(len(angles)):
                    if rotation_mode[i]:
                        angles[i] -= np.pi / ANGLE_FACTOR * dt / FPS
                        angles[i] = angles[i] if angles[i] > -2 * np.pi else -2 * np.pi
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

    handle_light_control()

    if rotating:
        if rotation_mode[0]:
            object = object.rotateX(sign * angles[0])
        if rotation_mode[1]:
            object = object.rotateY(sign * angles[1])
        if rotation_mode[2]:
            object = object.rotateZ(sign * angles[2])
        projected_object = object.translate([0, 0, OFFSET], copy=True).illuminate(light, intensity=intensity).project(AR, FOV, FAR, NEAR)
    if light_changed:
        if not(any(light_control_holds)):
            light_changed = False
        projected_object = object.translate([0, 0, OFFSET], copy=True).illuminate(light, intensity=intensity).project(AR, FOV, FAR, NEAR)

    # Clear screen
    fill_background()
    # Draw geometry
    projected_object.prepare(screen, copy=True).draw(screen, wireframe=wireframe)
    # Draw angles, light source and intensity information
    draw_text()

    # Update screen
    pygame.display.update()
    dt = clock.tick(60)

