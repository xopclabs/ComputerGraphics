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
# Colors
BG_COLOR = (0, 0, 0)
OBJECT_COLOR = (255, 255, 255)
BOX_COLOR = (100, 100, 100)
# Interface
FPS = 60

# pygame initialization
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
dt = 0
# Screen settings
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('[4] Leyba Rusakov Urban')
# Font for text rendering
font = pygame.font.SysFont('mononoki Nerd Font', 15)

# Polygon generation
def generate_polygon():
    poly = np.array([
        # Left top
        [
            np.random.randint(SCREEN_WIDTH // 5, 1.5 * SCREEN_WIDTH // 5),
            np.random.randint(SCREEN_HEIGHT // 5, 2 * SCREEN_HEIGHT // 5),
        ],
        # Middle top
        [
            np.random.randint(1.5 * SCREEN_WIDTH // 5, 2 * SCREEN_WIDTH // 5),
            np.random.randint(SCREEN_HEIGHT // 5, 2 * SCREEN_HEIGHT // 5),
        ],
        # Right top
        [
            np.random.randint(2 * SCREEN_WIDTH // 5, 4 * SCREEN_WIDTH // 5),
            np.random.randint(SCREEN_HEIGHT // 5, 2 * SCREEN_HEIGHT // 5),
        ],
        # Right bottom
        [
            np.random.randint(2 * SCREEN_WIDTH // 5, 4 * SCREEN_WIDTH // 5),
            np.random.randint(2 * SCREEN_HEIGHT // 5, 4 * SCREEN_HEIGHT // 5),
        ],
        # Middle bottom
        [
            np.random.randint(1.5 * SCREEN_WIDTH // 5, 2 * SCREEN_WIDTH // 5),
            np.random.randint(2 * SCREEN_HEIGHT // 5, 4 * SCREEN_HEIGHT // 5),
        ],
        # Left bottom
        [
            np.random.randint(SCREEN_WIDTH // 5, 1.5 * SCREEN_WIDTH // 5),
            np.random.randint(2 * SCREEN_HEIGHT // 5, 4 * SCREEN_HEIGHT // 5),
        ]
    ])
    print(poly.shape)
    return poly


def draw_polygon():
    for i in range(len(polygon) - 1):
        pygame.draw.line(screen, OBJECT_COLOR, polygon[i], polygon[i + 1])
    pygame.draw.line(screen, OBJECT_COLOR, polygon[0], polygon[-1])


def draw_rect():
    pygame.draw.line(screen, BOX_COLOR, [rect_x1, rect_y1], [rect_x1, rect_y2])
    pygame.draw.line(screen, BOX_COLOR, [rect_x1, rect_y2], [rect_x2, rect_y2])
    pygame.draw.line(screen, BOX_COLOR, [rect_x2, rect_y2], [rect_x2, rect_y1])
    pygame.draw.line(screen, BOX_COLOR, [rect_x2, rect_y1], [rect_x1, rect_y1])

def fill_background():
    screen.fill(BG_COLOR)


polygon = generate_polygon()
rect_x1, rect_y1, rect_x2, rect_y2 = 0, 0, 0, 0
moving = False
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
                polygon = generate_polygon()
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect_x1, rect_y1 = pygame.mouse.get_pos()
            moving = True
        if event.type == pygame.MOUSEMOTION:
            if moving:
                rect_x2, rect_y2 = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            moving = False

    # Clear screen
    fill_background()
    # Draw geometry
    draw_polygon()
    draw_rect()

    # Update screen
    pygame.display.update()
    dt = clock.tick(60)
