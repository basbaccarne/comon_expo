# This is the main script for the COMON expo robot
# It manages button presses (votes on a public display) and shows summary results using PyGame

# ACTIVE CAMPAIGN
# (change filename to start a new campaign)
active_campaign = "votes_test.json"

# LIBRARIES
import pygame
import json
import random
import time
from time import sleep
from gpiozero import Button
from pathlib import Path

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
# screen_info = pygame.display.Info()
# SCREEN_WIDTH = screen_info.current_w
# SCREEN_HEIGHT = screen_info.current_h
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
VOTE_FILE = DATA_DIR / active_campaign

# DESIGN
WHITE = (255, 255, 255)
BG_COLOR = (12, 37, 84)
LINE_COLOR = (200, 100, 50)
FONT = pygame.font.Font(FONT_PATH, 100)
pygame.mouse.set_visible(False)

# GLOBAL VARIABLES
state = "question"
timer = 0

# FUNCTIONAL FUNCTIONS
def load_votes():
    """Load previous votes if available"""
    try:
        with open(VOTE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"button1": 0, "button2": 0, "button3": 0}


def count_votes(button):
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
        
def drawLine(point1, point2, point3, color):
    """draw a line between 3 points"""
    pygame.draw.line(screen, color, point1, point2, 5)
    pygame.draw.line(screen, color, point2, point3, 5)


# STATE FUNCTIONS #
###################

# STATE: QUESTION
def main_question():
    """Display the main question screen (static)"""

    # background
    screen.fill(BG_COLOR)

    # text
    line1 = FONT.render("?", True, WHITE)
    line2 = FONT.render(" ", True, WHITE)
    rotated_line1 = pygame.transform.rotate(line1, 90)
    rotated_line2 = pygame.transform.rotate(line2, 90)
    line1_rect = rotated_line1.get_rect(center=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
    line2_rect = rotated_line2.get_rect(center=(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2))
    screen.blit(rotated_line1, line1_rect)
    screen.blit(rotated_line2, line2_rect)

    # lines
    drawLine((100,0),(400,SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2), WHITE)
    drawLine((100,SCREEN_HEIGHT),(400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2),WHITE)
    drawLine((SCREEN_WIDTH-100,SCREEN_HEIGHT),(SCREEN_WIDTH-400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2+100,SCREEN_HEIGHT//2), WHITE)

    # render
    pygame.display.flip()

# STATE: RESPONSE ANIMATION
def response_animation(button):
    """Animate the response screen"""

    # change line color of the selected option
    if button == 1:
        drawLine((100,0),(400,SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2), LINE_COLOR)
    if button == 2:
        drawLine((100,SCREEN_HEIGHT),(400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2), LINE_COLOR)
    if button == 3:
        drawLine((SCREEN_WIDTH-100,SCREEN_HEIGHT),(SCREEN_WIDTH-400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2+100,SCREEN_HEIGHT//2), LINE_COLOR)
    
    # render
    pygame.display.update()

# STATE: RESPONSE
def response_screen():
    """Display the response screen (static)"""

    # background
    screen.fill(BG_COLOR)

    # rectangles
    rect_agree = pygame.Rect(0, 0, 500, 400)
    rect_agree.center = (SCREEN_WIDTH // 1.3 , SCREEN_HEIGHT // 2)
    rect_disagree = pygame.Rect(0, 0, 450, 400)
    rect_disagree.center = (SCREEN_WIDTH //2 , SCREEN_HEIGHT // 2)
    rect_noopinion = pygame.Rect(0, 0, 600, 400)
    rect_noopinion.center = (400 , SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, WHITE, rect_agree, border_radius=40)
    pygame.draw.rect(screen, WHITE, rect_disagree, border_radius=40)
    pygame.draw.rect(screen, WHITE, rect_noopinion, border_radius=40)

    # render
    pygame.display.flip()


# PRELOADING #
##############

# Load JSON file with from previous sessions
votes = load_votes()
print("Current votes:", votes)

# Preload first screen
main_question()


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
        if button1.is_pressed:
            count_votes(1)
            change_state("response_animation")
            response_animation(pressed)
            
        if button2.is_pressed:
            count_votes(2)
            change_state("response_animation")
            response_animation(pressed)         
            
        if button3.is_pressed:
            count_votes(3)
            change_state("response_animation")
            response_animation(pressed)

    # STATE: RESPONSE_ANIMATION
    if state == "response_animation":
        # wait 2 seconds, then change state
        if pygame.time.get_ticks() / 1000 - timer > 2:
            change_state("response")
            response_screen()

    # STATE: RESPONSE SCREEN
    if state == "response":
        # wait 2 seconds, then change state
        if pygame.time.get_ticks() / 1000 - timer > 2:
            change_state("question")
            main_question()
            

    # Limit the frame rate
    clock.tick(FPS)

pygame.quit()
