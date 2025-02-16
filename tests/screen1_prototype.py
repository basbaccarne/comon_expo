# This is the visual design for screen 1

# modules
import pygame
import pygvideo
from pathlib import Path

import os
os.environ['PULSE_SERVER'] = ''

# Initialize Pygame
pygame.init()

# FPS (PyGame)
FPS = 20

# display set-up
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
pygame.display.set_caption("Comon Expo Interface")
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.FULLSCREEN | pygame.DOUBLEBUF,
    vsync=1)

# PATHS
SCRIPT_DIR = Path(__file__).parent

DATA_DIR = SCRIPT_DIR.parent / 'data'
FONT_PATH = DATA_DIR / 'TT Firs Neue Regular.ttf'

IMG_DIR = SCRIPT_DIR.parent / 'img'
GREEN_IMG = IMG_DIR / 'groen_lijn_1.png'
AKKOORD = IMG_DIR / 'akkoord_1.png'
RED_IMG = IMG_DIR / 'rood_lijn_1.png'
NIETAKKOORD = IMG_DIR / 'nietakkoord_1.png'
YELLOW_IMG = IMG_DIR / 'geel_lijn_1.png'
GEENMENING = IMG_DIR / 'geenmening_1.png'
VIDEO = IMG_DIR / 'animation.mkv'

# DESIGN
WHITE = (255, 255, 255)
BG_COLOR = (102, 203, 187)
DARKBLUE = (27, 60, 127)
GREEN = (0, 191, 98)
RED = (255, 49, 49)
GREEN = (0, 191, 98)
YELLOW = (255, 222, 89)
LINE_COLOR = (200, 100, 50)
FONT = pygame.font.Font(FONT_PATH, 70)
VIDEO_SIZE = (800, 800)
pygame.mouse.set_visible(False)

# STATE: QUESTION
def main_question():
    """Display the main question screen (static)"""

    # background
    # screen.fill(BG_COLOR)

    # text scene 1 (instructies)
    text_position1 = (400, SCREEN_HEIGHT // 2)
    text_position2 = (500, SCREEN_HEIGHT // 2)
    line1 = FONT.render("Geef je mening door QBot", True, DARKBLUE)
    line2 = FONT.render("een high five te geven", True, DARKBLUE)
    rotated_line1 = pygame.transform.rotate(line1, 90)
    rotated_line2 = pygame.transform.rotate(line2, 90)
    line1_rect = rotated_line1.get_rect(center=text_position1)
    line2_rect = rotated_line2.get_rect(center=text_position2)
    screen.blit(rotated_line1, line1_rect)
    screen.blit(rotated_line2, line2_rect)

    # end of the lines (x, y, reverse)
    position_green_line = (40, 0)
    position_red_line = (1700, 280)
    position_yellow_line = (1380, 800)

    screen.blit(line_green, position_green_line)
    screen.blit(line_red, position_red_line)
    screen.blit(line_yellow, position_yellow_line)

    # vote text
    position_akkooord = (40, 85)
    position_niet_akkooord = (1700, 350)
    position_geen_mening = (1350, 500)

    screen.blit(akkoord, position_akkooord)
    screen.blit(niet_akkoord, position_niet_akkooord)
    screen.blit(geen_mening, position_geen_mening)

    # render
    # pygame.display.flip()

# PRELOADING #
##############

# Load images (line peaces) // rotate (rescale if needed)
line_green = pygame.image.load(GREEN_IMG).convert_alpha()
line_green = pygame.transform.rotate(line_green, 90)

line_red = pygame.image.load(RED_IMG).convert_alpha()
line_red = pygame.transform.rotate(line_red, 90)

line_yellow = pygame.image.load(YELLOW_IMG).convert_alpha()
line_yellow = pygame.transform.rotate(line_yellow, 90)

akkoord = pygame.image.load(AKKOORD).convert_alpha()
akkoord = pygame.transform.rotate(akkoord, 90)

niet_akkoord = pygame.image.load(NIETAKKOORD).convert_alpha()
niet_akkoord = pygame.transform.rotate(niet_akkoord, 90)

geen_mening = pygame.image.load(GEENMENING).convert_alpha()
geen_mening = pygame.transform.rotate(geen_mening, 90)

# load video
video = pygvideo.Video(VIDEO)
video.set_size(VIDEO_SIZE)
video.preplay(-1)
video_width, video_height = video.get_size()
center_x = (SCREEN_WIDTH - video_width) // 2
center_y = (SCREEN_HEIGHT - video_height) // 2

# Preload first screen
main_question()

# MAIN GAME LOOP #
##################

clock = pygame.time.Clock()
running = True

main_question()

while running:

    # Exit the progam on ctrl + C
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        video.handle_event(event)

    # STATE MACHINE #
    #################

    # STATE: QUESTION

    # STATE: RESPONSE_ANIMATION

    # STATE: RESPONSE SCREEN
    
    
    screen.fill(BG_COLOR)
    video.draw_and_update(screen, (center_x, center_y))
    main_question()
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FPS)

pygvideo.quit_all()
pygame.quit()
