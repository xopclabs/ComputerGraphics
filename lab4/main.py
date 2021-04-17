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
CLIPPED_COLOR = BOX_COLOR
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

line = None
clipped = None
rect_left_x, rect_top_y, rect_right_x, rect_bot_y = 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT
moving = False

# Polygon generation
def generate_line():
    l = np.array([
        [
            [
                np.random.randint(SCREEN_WIDTH // 5, 1.5 * SCREEN_WIDTH // 5),
                np.random.randint(SCREEN_HEIGHT // 5, 2 * SCREEN_HEIGHT // 5),
            ],
            [
                np.random.randint(1.5 * SCREEN_WIDTH // 5, 2 * SCREEN_WIDTH // 5),
                np.random.randint(SCREEN_HEIGHT // 5, 2 * SCREEN_HEIGHT // 5),
            ],
        ],
        [
            [
                np.random.randint(2 * SCREEN_WIDTH // 5, 4 * SCREEN_WIDTH // 5),
                np.random.randint(SCREEN_HEIGHT // 5, 2 * SCREEN_HEIGHT // 5),
            ],
            [
                np.random.randint(2 * SCREEN_WIDTH // 5, 4 * SCREEN_WIDTH // 5),
                np.random.randint(2 * SCREEN_HEIGHT // 5, 4 * SCREEN_HEIGHT // 5),
            ],
        ],
        [
            [
                np.random.randint(1.5 * SCREEN_WIDTH // 5, 2 * SCREEN_WIDTH // 5),
                np.random.randint(2 * SCREEN_HEIGHT // 5, 4 * SCREEN_HEIGHT // 5),
            ],
            [
                np.random.randint(SCREEN_WIDTH // 5, 1.5 * SCREEN_WIDTH // 5),
                np.random.randint(2 * SCREEN_HEIGHT // 5, 4 * SCREEN_HEIGHT // 5),
            ]
        ]
    ])
    print(l.shape)
    return l


def draw_line(line, color=OBJECT_COLOR):
    if line == []:
        return
    for l in line:
        pygame.draw.line(screen, color, l[0], l[1])


def draw_rect():
    pygame.draw.line(screen, BOX_COLOR, [rect_left_x, rect_top_y], [rect_left_x, rect_bot_y])
    pygame.draw.line(screen, BOX_COLOR, [rect_left_x, rect_bot_y], [rect_right_x, rect_bot_y])
    pygame.draw.line(screen, BOX_COLOR, [rect_right_x, rect_bot_y], [rect_right_x, rect_top_y])
    pygame.draw.line(screen, BOX_COLOR, [rect_right_x, rect_top_y], [rect_left_x, rect_top_y])


def fill_background():
    screen.fill(BG_COLOR)


def get_code(p):
    code = 0
    if p[0] < rect_left_x:
        code |= 1
    elif p[0] > rect_right_x:
        code |= 2
    if p[1] > rect_bot_y:
        code |= 4
    elif p[1] < rect_top_y:
        code |= 8
    return code


def clip(p1, p2):
    code1, code2 = get_code(p1), get_code(p2)

    while True:
        if code1 == 0 and code2 == 0:
            return p1, p2
        elif code1 & code2:
            return None
        else:
            code = max(code1, code2)

            if code & 8:
                x = p1[0] + (p2[0] - p1[0]) * (rect_top_y - p1[1]) / (p2[1] - p1[1])
                y = rect_top_y
            elif code & 4:
                x = p1[0] + (p2[0] - p1[0]) * (rect_bot_y - p1[1]) / (p2[1] - p1[1])
                y = rect_bot_y
            elif code & 2:
                y = p1[1] + (p2[1] - p1[1]) * (rect_right_x - p1[0]) / (p2[0] - p1[0])
                x = rect_right_x
            elif code & 1:
                y = p1[1] + (p2[1] - p1[1]) * (rect_left_x - p1[0]) / (p2[0] - p1[0])
                x = rect_left_x

            if code == code1:
                p1 = [x, y]
                code1 = get_code(p1)
            else:
                p2 = [x, y]
                code2 = get_code(p2)


def clip_line(line):
    clipped_l = []

    for l in line:
        cl = clip(*l)
        if cl is not None:
            clipped_l.append(cl)
    return clipped_l


line = generate_line()
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
                line = generate_line()
                clipped = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect_left_x, rect_top_y = pygame.mouse.get_pos()
            moving = True
        if event.type == pygame.MOUSEMOTION:
            if moving:
                rect_right_x, rect_bot_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            moving = False
            if rect_left_x > rect_right_x:
                rect_left_x, rect_right_x = rect_right_x, rect_left_x
            if rect_top_y > rect_bot_y:
                rect_top_y, rect_bot_y = rect_bot_y, rect_top_y
            clipped = clip_line(line)
            print(clipped)

    # Clear screen
    fill_background()
    # Draw geometry
    if clipped is not None:
        draw_line(line, CLIPPED_COLOR)
        draw_line(clipped)
    else:
        draw_line(line)

    draw_rect()

    # Update screen
    pygame.display.update()
    dt = clock.tick(60)
