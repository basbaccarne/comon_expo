# This script ...

import pygame
import time
from pathlib import Path

# Initialize Pygame
pygame.init()

# FPS
FPS = 60

# PATHS
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / 'data'
FONT_PATH = DATA_DIR / 'TT Firs Neue Regular.ttf'

# DESIGN
WHITE = (255, 255, 255)
BG_COLOR = (12, 37, 84)
FONT = pygame.font.Font(FONT_PATH, 100)
pygame.mouse.set_visible(False)

# SCREEN SIZE
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# GLOBAL VARIABLES

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                  pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED,
                                  vsync=1)
pygame.display.set_caption("Comon Expo Interface")

# Precalculations & preload
def mainQuestion():
    line1 = FONT.render("Kweetnieoecoole", True, WHITE)
    line2 = FONT.render("vraag", True, WHITE)
    rotated_line1 = pygame.transform.rotate(line1, 90)
    rotated_line2 = pygame.transform.rotate(line2, 90)
    line1_rect = rotated_line1.get_rect(center=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
    line2_rect = rotated_line2.get_rect(center=(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2))

    screen.fill(BG_COLOR)
    screen.blit(rotated_line1, line1_rect)
    screen.blit(rotated_line2, line2_rect)

    pygame.display.flip()


mainQuestion()

# Animation loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Do stuff

    # Limit the frame rate
    clock.tick(FPS)

pygame.quit()
