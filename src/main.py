# This is the main script for the COMON expo robot
# It manages button presses (votes on a public display) and shows summary results using PyGame

# ACTIVE CAMPAIGN
# (change filename to start a new campaign)
active_campaign = "votes_test.json"

# LIBRARIES
import pygame
import pygvideo
import json
import random
import time
from time import sleep
from gpiozero import Button
from pathlib import Path
import os

# GPIO button setup
# (buttons are connected to ground and pins 4, 14 and 25)
button1 = Button(4)
button2 = Button(14)
button3 = Button(25)

# Initialize Pygame
pygame.init()

# FPS (PyGame)
FPS = 60

# DISPLAY SET-UP
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
pygame.display.set_caption("Comon Expo Interface")
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.FULLSCREEN | pygame.DOUBLEBUF,
    vsync=1)

# PATHS
SCRIPT_DIR = Path(__file__).parent

DATA_DIR = SCRIPT_DIR.parent / 'data'
VOTE_FILE = DATA_DIR / active_campaign

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
FONT = pygame.font.Font(FONT_PATH, 100)
VIDEO_SIZE = (800, 800)
pygame.mouse.set_visible(False)

# GLOBAL VARIABLES
state = "question"
timer = 0
circle_radius = 0
pressed = None

# FUNCTIONAL FUNCTIONS
def load_votes():
    """Load previous votes if available"""
    try:
        with open(VOTE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"button1": 0, "button2": 0, "button3": 0}


def count_votes(button):
    """Count votes and save to file"""
    global votes, pressed

    # count votes
    if button == 1:
        votes["button1"] += 1
        pressed = 1
    if button == 2:
        votes["button2"] += 1
        pressed = 2
    if button == 3:
        votes["button3"] += 1
        pressed = 3
    print(f"Button {button} pressed.")
    print("Total votes: [1] ", votes["button1"], " || [2] ", votes["button2"], " || [3] ", votes["button3"])

    # save votes
    save_votes(votes)

def change_state(new_state):
    global timer, state
    timer = pygame.time.get_ticks() / 1000
    state = new_state
    print(f"State: {state}")

def save_votes(votes):
    """Save vote counts to file"""
    with open(VOTE_FILE, 'w') as file:
        json.dump(votes, file)


# STATE FUNCTIONS #
###################

# STATE: QUESTION
def main_question():
    """Display the main question screen"""

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

    # end of the lines pngs
    position_green_line = (40, 0)
    position_red_line = (1700, 280)
    position_yellow_line = (1380, 800)
    screen.blit(line_green, position_green_line)
    screen.blit(line_red, position_red_line)
    screen.blit(line_yellow, position_yellow_line)

    # vote choice pngs
    position_akkooord = (40, 85)
    position_niet_akkooord = (1700, 350)
    position_geen_mening = (1350, 500)
    screen.blit(akkoord, position_akkooord)
    screen.blit(niet_akkoord, position_niet_akkooord)
    screen.blit(geen_mening, position_geen_mening)

# STATE: RESPONSE ANIMATION
def response_animation(button, circle_radius):
    """Animate the response screen"""

    color = DARKBLUE
    position = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    # draw circle (this one will grow)
    pygame.draw.circle(screen, color, position, circle_radius)

    # text (selected choice)
    if button == 1:
        choice = '[ AKKOORD ]'
    elif button == 2:
        choice = '[ NIET AKKOORD ]'
    elif button == 3:
        choice = '[ GEEN MENING ]'

    # draw text once the circle is big enough
    if circle_radius > 400:
        text_position1 = (SCREEN_WIDTH//2-50, SCREEN_HEIGHT // 2)
        text_position2 = (SCREEN_WIDTH//2+50, SCREEN_HEIGHT // 2)
        line1 = FONT.render("Jouw standpunt", True, WHITE)
        line2 = FONT.render(choice, True, WHITE)
        rotated_line1 = pygame.transform.rotate(line1, 90)
        rotated_line2 = pygame.transform.rotate(line2, 90)
        line1_rect = rotated_line1.get_rect(center=text_position1)
        line2_rect = rotated_line2.get_rect(center=text_position2)
        screen.blit(rotated_line1, line1_rect)
        screen.blit(rotated_line2, line2_rect)

# STATE: RESPONSE
def response_screen():
    """Display the response screen (static)"""
    global votes, pressed

    # calculate percentages (the numbers)
    total=votes["button1"]+votes["button2"]+votes["button3"]
    agree = votes["button1"]/total*100
    disagree = votes["button2"]/total*100
    noopinion = votes["button3"]/total*100

    # padding & fixed design parameters
    inner_padding = 20 # padding between rectangles
    outer_padding = 40 # padding from the edge of the screen
    fixed_width = 1000 # bar width

    # calculate heights
    total_container_height = SCREEN_WIDTH - outer_padding * 2 # outer bounds
    centered_position = SCREEN_HEIGHT // 2 - fixed_width // 2 # center for the y axis

    agree_height     = (total_container_height * agree / 100) - inner_padding
    disagree_height  = (total_container_height * disagree / 100) - inner_padding
    noopinion_height = (total_container_height * noopinion / 100) - inner_padding

    # background
    screen.fill(BG_COLOR)

    # result rectangles (x, y, width, height)
    rect_agree = pygame.Rect(
        outer_padding, centered_position, 
        agree_height, fixed_width)
    rect_disagree = pygame.Rect(
        outer_padding + agree_height + inner_padding * 1.5, centered_position, 
        disagree_height, fixed_width)
    rect_noopinion = pygame.Rect(
        outer_padding + agree_height + inner_padding * 1.5 + disagree_height + inner_padding * 1.5 , centered_position, 
        noopinion_height, fixed_width)
    pygame.draw.rect(screen, WHITE, rect_agree, border_radius=40)
    if pressed == 1:
        pygame.draw.rect(screen, DARKBLUE, rect_agree, border_radius=40)
    pygame.draw.rect(screen, WHITE, rect_disagree, border_radius=40)
    if pressed == 2:
        pygame.draw.rect(screen, DARKBLUE, rect_disagree, border_radius=40)
    pygame.draw.rect(screen, WHITE, rect_noopinion, border_radius=40)
    if pressed == 3:
        pygame.draw.rect(screen, DARKBLUE, rect_noopinion, border_radius=40)

    # text
    font = pygame.font.Font(FONT_PATH, 50)
    text_agree = font.render(f"{int(agree)}%", True, BG_COLOR)
    text_disagree = font.render(f"{int(disagree)}%", True, BG_COLOR)
    text_noopinion = font.render(f"{int(noopinion)}%", True, BG_COLOR)

    # rotate text
    rotated_text_agree = pygame.transform.rotate(text_agree, 90)
    rotated_text_disagree = pygame.transform.rotate(text_disagree, 90)
    rotated_text_noopinion = pygame.transform.rotate(text_noopinion, 90)

    # center text
    text_agree_rect = rotated_text_agree.get_rect(center=rect_agree.center)
    text_disagree_rect = rotated_text_disagree.get_rect(center=rect_disagree.center)
    text_noopinion_rect = rotated_text_noopinion.get_rect(center=rect_noopinion.center)

    # render text
    screen.blit(rotated_text_agree, text_agree_rect)
    screen.blit(rotated_text_disagree, text_disagree_rect)
    screen.blit(rotated_text_noopinion, text_noopinion_rect)

    # render
    pygame.display.flip()


# PRELOADING #
##############

# Load JSON file with from previous sessions
votes = load_votes()
print("Current votes:", votes)

# SCENE 1: Load images (line peaces) & rotate 90 degrees
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

# SCENE 1: load video
video = pygvideo.Video(VIDEO)
video.set_size(VIDEO_SIZE)
video.preplay(-1)
video_width, video_height = video.get_size()
center_x = (SCREEN_WIDTH - video_width) // 2
center_y = (SCREEN_HEIGHT - video_height) // 2

# Preload first screen
screen.fill(BG_COLOR)
main_question()
pygame.display.flip()

# MAIN GAME LOOP #
##################

clock = pygame.time.Clock()
running = True

while running:

    # Exit the progam on ctrl + C
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # STATE MACHINE #
    #################

    # STATE: QUESTION
    # (listen to the buttons when the systel is in the question state)
    if state == "question":
        screen.fill(BG_COLOR)
        video.draw_and_update(screen, (center_x, center_y))
        main_question()
        pygame.display.flip()

        if button1.is_pressed:
            count_votes(1)
            pressed = 1
            circle_radius = 0
            change_state("response_animation")
            
        if button2.is_pressed:
            count_votes(2)
            pressed = 2
            circle_radius = 0
            change_state("response_animation")
            
        if button3.is_pressed:
            count_votes(3)
            pressed = 3
            circle_radius = 0
            change_state("response_animation")

    # STATE: RESPONSE_ANIMATION
    if state == "response_animation":
        growth_speed = 50
        circle_radius += growth_speed
        response_animation(pressed, circle_radius)

        # wait 2 seconds, then change state
        if pygame.time.get_ticks() / 1000 - timer > 2:
            change_state("response")
            response_screen()

    # STATE: RESPONSE SCREEN
    if state == "response":
        # wait 2 seconds, then change state
        if pygame.time.get_ticks() / 1000 - timer > 4:
            change_state("question")
            main_question()
            

    # Limit the frame rate
    clock.tick(FPS)

pygvideo.quit_all()
pygame.quit()
