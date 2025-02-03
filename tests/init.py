# This script ...

import pygame
import random
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
LINE_COLOR = (200, 100, 50)
FONT = pygame.font.Font(FONT_PATH, 100)
pygame.mouse.set_visible(False)

# SCREEN SIZE
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# GLOBAL VARIABLES
state = "question"
old_state = state


# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                  pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED,
                                  vsync=1)
pygame.display.set_caption("Comon Expo Interface")

# Functions
def mainQuestion():
    line1 = FONT.render("?", True, WHITE)
    line2 = FONT.render(" ", True, WHITE)
    rotated_line1 = pygame.transform.rotate(line1, 90)
    rotated_line2 = pygame.transform.rotate(line2, 90)
    line1_rect = rotated_line1.get_rect(center=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
    line2_rect = rotated_line2.get_rect(center=(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2))

    screen.fill(BG_COLOR)
    screen.blit(rotated_line1, line1_rect)
    screen.blit(rotated_line2, line2_rect)

def drawLine(point1, point2, point3):
    pygame.draw.line(screen, WHITE, point1, point2, 5)
    pygame.draw.line(screen, WHITE, point2, point3, 5)
    

# Preload
mainQuestion()
drawLine((100,0),(400,SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2))
drawLine((100,SCREEN_HEIGHT),(400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2))
drawLine((SCREEN_WIDTH-100,SCREEN_HEIGHT),(SCREEN_WIDTH-400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2+100,SCREEN_HEIGHT//2))

pygame.display.flip()


# Animation loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # state swicher
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            state = "response" if state == "question" else "question"
            print(f"State: {state}")
            if state == "question":
                mainQuestion()
                drawLine((100,0),(400,SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2))
                drawLine((100,SCREEN_HEIGHT),(400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2))
                drawLine((SCREEN_WIDTH-100,SCREEN_HEIGHT),(SCREEN_WIDTH-400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2+100,SCREEN_HEIGHT//2))

                pygame.display.flip()

            elif state == "response":
                screen.fill(BG_COLOR)
                
                rect_agree = pygame.Rect(0, 0, 500, 400)
                rect_agree.center = (SCREEN_WIDTH // 1.3 , SCREEN_HEIGHT // 2)

                rect_disagree = pygame.Rect(0, 0, 450, 400)
                rect_disagree.center = (SCREEN_WIDTH //2 , SCREEN_HEIGHT // 2)

                rect_noopinion = pygame.Rect(0, 0, 600, 400)
                rect_noopinion.center = (400 , SCREEN_HEIGHT // 2)

                pygame.draw.rect(screen, WHITE, rect_agree, border_radius=40)
                pygame.draw.rect(screen, WHITE, rect_disagree, border_radius=40)
                pygame.draw.rect(screen, WHITE, rect_noopinion, border_radius=40)
                pygame.display.flip()
    

    # Do stuff

    # Limit the frame rate
    clock.tick(FPS)

pygame.quit()
