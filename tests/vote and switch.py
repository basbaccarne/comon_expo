# This script is used to test the interface of the common expo
# It is a simple interface that shows a question mark and then switches to a response screen when a button is pressed

# change filename to start a new campaign
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
# buttons are connected to ground and pins 4, 14 and 25
button1 = Button(4)
button2 = Button(14)
button3 = Button(25)

# Initialize Pygame
pygame.init()

# FPS
FPS = 60

# Set up the display
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                  pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED,
                                  vsync=1)
pygame.display.set_caption("Comon Expo Interface")

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
old_state = state
timer = 0

# FUNCTIONS
def load_votes():
    """Load previous votes if available"""
    try:
        with open(VOTE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"button1": 0, "button2": 0, "button3": 0}


def save_votes(votes):
    """Save vote counts to file"""
    with open(VOTE_FILE, 'w') as file:
        json.dump(votes, file)
        
def drawLine(point1, point2, point3, color):
    """draw a line between 3 points"""
    pygame.draw.line(screen, color, point1, point2, 5)
    pygame.draw.line(screen, color, point2, point3, 5)
        


def mainQuestion():
    """Display the main question screen"""
    line1 = FONT.render("?", True, WHITE)
    line2 = FONT.render(" ", True, WHITE)
    rotated_line1 = pygame.transform.rotate(line1, 90)
    rotated_line2 = pygame.transform.rotate(line2, 90)
    line1_rect = rotated_line1.get_rect(center=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
    line2_rect = rotated_line2.get_rect(center=(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2))

    screen.fill(BG_COLOR)
    screen.blit(rotated_line1, line1_rect)
    screen.blit(rotated_line2, line2_rect)

    drawLine((100,0),(400,SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2), WHITE)
    drawLine((100,SCREEN_HEIGHT),(400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2),WHITE)
    drawLine((SCREEN_WIDTH-100,SCREEN_HEIGHT),(SCREEN_WIDTH-400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2+100,SCREEN_HEIGHT//2), WHITE)

    pygame.display.flip()

def responseScreen():
    """Display the response screen"""
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

def response_animation(button):
    """Animate the response screen"""
    if button == 1:
        drawLine((100,0),(400,SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2), LINE_COLOR)
        pygame.display.update()
    if button == 2:
        drawLine((100,SCREEN_HEIGHT),(400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2), LINE_COLOR)
        pygame.display.update()
    if button == 3:
        drawLine((SCREEN_WIDTH-100,SCREEN_HEIGHT),(SCREEN_WIDTH-400,SCREEN_HEIGHT-SCREEN_HEIGHT//4),(SCREEN_WIDTH//2+100,SCREEN_HEIGHT//2), LINE_COLOR)
        pygame.display.update()
        

# PRELOADING

# Initialize vote counts
votes = load_votes()
print("Current votes:", votes)

# Preload first screen
mainQuestion()

# MAIN GAME LOOP

clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # state swicher (keyboard version)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            state = "response" if state == "question" else "question"
            print(f"State: {state}")
            if state == "question":
                mainQuestion()
            elif state == "response":
                responseScreen()

    # STATE SWICHER (button version)
    
    # STATE QUESTION
    # listen to the buttons when the systel is in the question state
    if state == "question":
        if button1.is_pressed:
            # count votes
            votes["button1"] += 1
            pressed = 1
            print("Button 1 pressed.")
            print("Total votes: [1] ", votes["button1"], " || [2] ", votes["button2"], " || [3] ", votes["button3"])
            save_votes(votes)
            
            # change state
            timer = pygame.time.get_ticks() / 1000
            state = "response_animation"
            print(f"State: {state}")
            
        if button2.is_pressed:
            # count votes
            votes["button2"] += 1
            pressed = 2
            print("Button 2 pressed.")
            print("Total votes: [1] ", votes["button1"], " || [2] ", votes["button2"], " || [3] ", votes["button3"])
            save_votes(votes)
            
            # change state
            timer = pygame.time.get_ticks() / 1000
            state = "response_animation"
            print(f"State: {state}")            
            
        if button3.is_pressed:
            # count votes
            votes["button3"] += 1
            pressed = 3
            print("Button 3 pressed.")
            print("Total votes: [1] ", votes["button1"], " || [2] ", votes["button2"], " || [3] ", votes["button3"])
            save_votes(votes)
            
            # change state
            timer = pygame.time.get_ticks() / 1000
            state = "response_animation"     
            print(f"State: {state}")

    # STATE RESPONSE ANIMATION
    if state == "response_animation":
        response_animation(pressed)

        if pygame.time.get_ticks() / 1000 - timer > 2:
            state = "response"
            print(f"State: {state}")
            timer = pygame.time.get_ticks() / 1000
            responseScreen()

    # STATE RESPONSE SCREEN
    if state == "response":
        if pygame.time.get_ticks() / 1000 - timer > 2:
            state = "question"
            print(f"State: {state}")
            timer = pygame.time.get_ticks()
            mainQuestion()
            

    # Limit the frame rate
    clock.tick(FPS)

pygame.quit()
