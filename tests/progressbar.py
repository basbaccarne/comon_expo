# This script runs a progress bar at the bottom of the screen.

# libs
import pygame
import time

# Initialize Pygame
pygame.init()

# FPS
FPS = 30

# display set-up
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
pygame.display.set_caption("Progress Bar")
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.FULLSCREEN | pygame.DOUBLEBUF,
    vsync=1)

# DESIGN
BG_COLOR = (102, 203, 187)
DARKBLUE = (27, 60, 127)
pygame.mouse.set_visible(False)

# GLOBAL VARIABLES
bar_height = 40
bar_width = SCREEN_WIDTH
bar_area = pygame.Rect(SCREEN_WIDTH - bar_height, 0,  bar_height, bar_width)
bin_width = 0
start_time = 0

def init_Progress_bar(time_duration):
    """Initialize the progress bar with the given duration."""
    global bin_width, start_time, duration

    # Render the background
    screen.fill(BG_COLOR)

    # Draw the initial progress bar
    pygame.draw.rect(screen, DARKBLUE, bar_area)
    pygame.display.update(bar_area)
    
    # Calculate bin width
    duration = time_duration
    bin_width = bar_width / time_duration
    start_time = time.time()

def update_progress_bar():
    """Update the progress bar based on elapsed time."""
    global last_update_time
    
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    progress_width = int((elapsed_time / duration) * bar_width)
    # elapsed_time = pygame.time.get_ticks()  - start_time

    if progress_width <= bar_width:
        retract_distance = bin_width * elapsed_time
        progress_rect = pygame.Rect(SCREEN_WIDTH-bar_height, 0, bar_height, retract_distance)    
        pygame.draw.rect(screen, BG_COLOR, progress_rect)

        pygame.display.update(progress_rect)

    
# Precalculations & preload
screen.fill(BG_COLOR)
pygame.display.update()
init_Progress_bar(20)

# Animation loop
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Update the progress bar
    update_progress_bar()

    # Limit the frame rate
    clock.tick(FPS)

pygame.quit()
