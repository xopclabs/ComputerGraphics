import numpy as np
import pygame
import os, sys
from spline import Spline


# Global settings
# Screen stuff
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_HEIGHT = SCREEN_HEIGHT // 2
# Colors
BG_COLOR = (0, 0, 0)
LINE_COLOR = (100, 100, 100)
SPLINE_COLOR = (255, 0, 0)
# Interface
FPS = 60

# pygame initialization
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
dt = 0
# Screen settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('[2] Leyba Rusakov Urban')

# Line definition
points = []

def draw_line(line, color=LINE_COLOR):
    if line == []:
        return
    for p in points:
        pygame.draw.circle(screen, color, p, 3)
    if len(line) >= 2:
        for i in range(1, len(line)):
            pygame.draw.line(screen, color, line[i - 1], line[i])


def fill_background():
    screen.fill(BG_COLOR)


points = []
spline = None
# Main loop
while True:
    # Event handling
    for event in pygame.event.get():
        # Quitting
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                points = []
                spline = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            points.append(list(pygame.mouse.get_pos()))
            if len(points) >= 8:
                spline = Spline(points).line

    # Clear screen
    fill_background()
    # Draw geometry
    draw_line(points)
    if spline is not None:
        draw_line(spline, SPLINE_COLOR)

    # Update screen
    pygame.display.update()
    dt = clock.tick(60)
