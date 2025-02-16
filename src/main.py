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
import os

# GPIO button setup
# (buttons are connected to ground and pins 4, 14 and 25)
button1 = Button(4)
button2 = Button(14)
button3 = Button(25)

# Initialize Pygame
pygame.init()

# FPS (PyGame)
FPS = 30

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
IMAGE_FOLDER = IMG_DIR / 'animation'

"""scene 1"""
GREEN_IMG = IMG_DIR / 'groen_lijn_1.png'
AKKOORD = IMG_DIR / 'akkoord_1.png'
RED_IMG = IMG_DIR / 'rood_lijn_1.png'
NIETAKKOORD = IMG_DIR / 'nietakkoord_1.png'
YELLOW_IMG = IMG_DIR / 'geel_lijn_1.png'
GEENMENING = IMG_DIR / 'geenmening_1.png'

"""scene 2"""
GREEN_TOP = IMG_DIR / 'top_green.png'
GREEN_BOTTOM = IMG_DIR / 'bottom_green.png'
RED_TOP = IMG_DIR / 'top_red.png'
RED_BOTTOM = IMG_DIR / 'bottom_red.png'
YELLOW_TOP = IMG_DIR / 'top_yellow.png'
YELLOW_BOTTOM = IMG_DIR / 'bottom_yellow.png'
AKKOORD_2 = IMG_DIR / 'akkoord_2.png'
NIETAKKOORD_2 = IMG_DIR / 'nietakkoord_2.png'
GEENMENING_2 = IMG_DIR / 'geenmening_2.png'
AKKOORD_2_SELECTED = IMG_DIR / 'akkoord_2_selected.png'
NIETAKKOORD_2_SELECTED = IMG_DIR / 'nietakkoord_2_selected.png'
GEENMENING_2_SELECTED = IMG_DIR / 'geenmening_2_selected.png'

# DESIGN
WHITE = (255, 255, 255)
BG_COLOR = (102, 203, 187)
DARKBLUE = (27, 60, 127)
GREEN = (0, 191, 98)
RED = (255, 49, 49)
GREEN = (0, 191, 98)
YELLOW = (255, 222, 89)
FONT = pygame.font.Font(FONT_PATH, 70)
RESCALE_VIDEO = (500,500)
pygame.mouse.set_visible(False)

# GLOBAL VARIABLES
"""state machine"""
state = "question"
timer = 0

"""reponse animation"""
circle_radius = 0
pressed = None

"""scene 2 timer"""
bar_height = 40
bar_width = SCREEN_WIDTH
bar_area = pygame.Rect(SCREEN_WIDTH - bar_height, 0,  bar_height, bar_width)
bin_width = 0
start_time = 0
pressed = 1

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

def init_Progress_bar(time_duration):
    """Initialize the progress bar with the given duration."""
    global bin_width, start_time, duration, start_ticks

    # Draw the initial progress bar
    pygame.draw.rect(screen, DARKBLUE, bar_area)
    
    # Calculate bin width
    duration = time_duration
    bin_width = bar_width / time_duration
    start_time = time.time()
    start_ticks = pygame.time.get_ticks()

def update_progress_bar():
    """Update the progress bar based on elapsed time."""
    global last_update_time
    
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    progress_width = int((elapsed_time / duration) * bar_width)

    if progress_width <= bar_width:
        retract_distance = bin_width * elapsed_time
        progress_rect = pygame.Rect(SCREEN_WIDTH-bar_height, 0, bar_height, retract_distance)    
        pygame.draw.rect(screen, BG_COLOR, progress_rect)

        pygame.display.update(progress_rect)

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

    # render
    pygame.display.update()

# STATE: RESPONSE
def response_screen():
    """Display the response screen (static)"""
    global votes, pressed

    # background
    screen.fill(BG_COLOR)

    # text scene 2 (zo denk jij versus de andere stemmers)
    text_position1 = (150, SCREEN_HEIGHT // 2)
    text_position2 = (250, SCREEN_HEIGHT // 2)
    line1 = FONT.render("Zo denk jij versus", True, DARKBLUE)
    line2 = FONT.render("de andere stemmers", True, DARKBLUE)
    rotated_line1 = pygame.transform.rotate(line1, 90)
    rotated_line2 = pygame.transform.rotate(line2, 90)
    line1_rect = rotated_line1.get_rect(center=text_position1)
    line2_rect = rotated_line2.get_rect(center=text_position2)
    screen.blit(rotated_line1, line1_rect)
    screen.blit(rotated_line2, line2_rect)

    # calculate percentages (the numbers)
    total=votes["button1"]+votes["button2"]+votes["button3"]
    agree = votes["button1"]/total
    disagree = votes["button2"]/total
    noopinion = votes["button3"]/total

    # fixed parameters for the bars
    starting_point = (400,250) # left corner of the green top
    bar_width = 449 # bar width
    size_ovals = (bar_width,121) # size of the ovals
    total_height = 1200 # total height of the stacked bars
    padding = 20 # padding between the bars
    
    # calculate bar widths based on JSON data
    green_height = agree * total_height - padding
    red_height = disagree * total_height - padding
    yellow_height = noopinion * total_height - padding

    # calculate all postions based on JSON data
    green_top_position = starting_point
    green_bar_position = ((starting_point[0]+size_ovals[1]//2), starting_point[1])
    green_bottom_position= ((green_bar_position[0]+green_height-size_ovals[1]//2), starting_point[1])

    yellow_top_position = (green_bottom_position[0]+padding, starting_point[1])
    yellow_bar_position = ((yellow_top_position[0]+size_ovals[1]//2), starting_point[1])
    yellow_bottom_position = ((yellow_bar_position[0]+yellow_height-size_ovals[1]//2), starting_point[1])

    red_top_position = (yellow_bottom_position[0]+padding, starting_point[1])
    red_bar_position = ((red_top_position[0]+size_ovals[1]//2), starting_point[1])
    red_bottom_position = ((red_bar_position[0]+red_height-size_ovals[1]//2), starting_point[1])

    label_akkoord_position = ((green_bar_position[0]+green_height//2), starting_point[1]+350)
    label_geenmening_position = ((yellow_bar_position[0]+yellow_height//2), starting_point[1]+350)
    label_nietakkoord_position = ((red_bar_position[0]+red_height//2), starting_point[1]+350)

    # draw the main graph
    screen.blit(red_bottom, red_bottom_position)
    rect_disagree = pygame.Rect(red_bar_position[0], red_bar_position[1], red_height, bar_width)
    pygame.draw.rect(screen, RED, rect_disagree)
    screen.blit(red_top, red_top_position)

    screen.blit(yellow_bottom, yellow_bottom_position)
    rect_noopinion = pygame.Rect(yellow_bar_position[0], yellow_bar_position[1], yellow_height, bar_width)
    pygame.draw.rect(screen, YELLOW, rect_noopinion)
    screen.blit(yellow_top, yellow_top_position)

    screen.blit(green_bottom, green_bottom_position)
    rect_agree = pygame.Rect(green_bar_position[0], green_bar_position[1], green_height, bar_width)
    pygame.draw.rect(screen, GREEN, rect_agree)
    screen.blit(green_top, green_top_position)

    # text for the percentages
    font = pygame.font.Font(FONT_PATH, 50)
    text_agree = font.render(f"{int(agree*100)}%", True, DARKBLUE)
    text_disagree = font.render(f"{int(disagree*100)}%", True, DARKBLUE)
    text_noopinion = font.render(f"{int(noopinion*100)}%", True, DARKBLUE)

    rotated_text_agree = pygame.transform.rotate(text_agree, 90)
    rotated_text_disagree = pygame.transform.rotate(text_disagree, 90)
    rotated_text_noopinion = pygame.transform.rotate(text_noopinion, 90)

    text_agree_rect = rotated_text_agree.get_rect(center=(rect_agree.center[0] + size_ovals[1]//2, rect_agree.center[1]))
    text_disagree_rect = rotated_text_disagree.get_rect(center=(rect_disagree.center[0] + size_ovals[1]//2, rect_disagree.center[1]))
    text_noopinion_rect = rotated_text_noopinion.get_rect(center=(rect_noopinion.center[0] + size_ovals[1]//2, rect_noopinion.center[1]))

    screen.blit(rotated_text_agree, text_agree_rect)
    screen.blit(rotated_text_disagree, text_disagree_rect)
    screen.blit(rotated_text_noopinion, text_noopinion_rect)

    # add graphical elements (akkoord - geen mening - niet akkoord)
    screen.blit(akkoord_2, label_akkoord_position)
    screen.blit(geenmening_2, label_geenmening_position)
    screen.blit(nietakkoord_2, label_nietakkoord_position)
    if pressed == 1:
        screen.blit(akkoord_2_selected, label_akkoord_position)
    elif pressed == 2:
        screen.blit(geenmening_2_selected, label_geenmening_position)
    elif pressed == 3:
        screen.blit(nietakkoord_2_selected, label_nietakkoord_position)

    # load progress bar (20 seconds)
    init_Progress_bar(20)

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
images = []
for file in sorted(os.listdir(IMAGE_FOLDER)):
    if file.endswith(".png"):
        img = pygame.image.load(os.path.join(IMAGE_FOLDER, file))
        images.append(img)

if not images:
    raise ValueError("No PNG images found in the specified folder.")

images = [pygame.transform.scale(img, RESCALE_VIDEO) for img in images]
center = ((SCREEN_WIDTH // 2) - (RESCALE_VIDEO[0]//2), (SCREEN_HEIGHT // 2) - (RESCALE_VIDEO[1]//2))

# SCENE 2: Load images
green_top = pygame.image.load(GREEN_TOP).convert_alpha()
green_top = pygame.transform.rotate(green_top, 90)
green_bottom = pygame.image.load(GREEN_BOTTOM).convert_alpha()
green_bottom = pygame.transform.rotate(green_bottom, 90)

red_top = pygame.image.load(RED_TOP).convert_alpha()
red_top = pygame.transform.rotate(red_top, 90)
red_bottom = pygame.image.load(RED_BOTTOM).convert_alpha()
red_bottom = pygame.transform.rotate(red_bottom, 90)

yellow_top = pygame.image.load(YELLOW_TOP).convert_alpha()
yellow_top = pygame.transform.rotate(yellow_top, 90)
yellow_bottom = pygame.image.load(YELLOW_BOTTOM).convert_alpha()
yellow_bottom = pygame.transform.rotate(yellow_bottom, 90)

akkoord_2 = pygame.image.load(AKKOORD_2).convert_alpha()
akkoord_2 = pygame.transform.rotate(akkoord_2, 90)
akkoord_2_selected = pygame.image.load(AKKOORD_2_SELECTED).convert_alpha()
akkoord_2_selected = pygame.transform.rotate(akkoord_2_selected, 90)
geenmening_2 = pygame.image.load(GEENMENING_2).convert_alpha()
geenmening_2 = pygame.transform.rotate(geenmening_2, 90)
geenmening_2_selected = pygame.image.load(GEENMENING_2_SELECTED).convert_alpha()
geenmening_2_selected = pygame.transform.rotate(geenmening_2_selected, 90)
nietakkoord_2 = pygame.image.load(NIETAKKOORD_2).convert_alpha()
nietakkoord_2 = pygame.transform.rotate(nietakkoord_2, 90)
nietakkoord_2_selected = pygame.image.load(NIETAKKOORD_2_SELECTED).convert_alpha()
nietakkoord_2_selected = pygame.transform.rotate(nietakkoord_2_selected, 90)

# Preload first screen
screen.fill(BG_COLOR)
main_question()
pygame.display.flip()

# MAIN GAME LOOP #
##################

clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
running = True
frame = 0

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

        # Display current video frame
        screen.blit(images[frame], center)
        pygame.display.update()
    
        # Update frame
        frame = (frame + 1) % len(images)

        # Check for button presses
        if not button1.is_pressed:
            count_votes(1)
            pressed = 1
            circle_radius = 0
            change_state("response_animation")
            
        if not button2.is_pressed:
            count_votes(2)
            pressed = 2
            circle_radius = 0
            change_state("response_animation")
            
        if not button3.is_pressed:
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
        if pygame.time.get_ticks() / 1000 - timer > 4:
            change_state("response")
            response_screen()
            pygame.display.flip()


    # STATE: RESPONSE SCREEN
    if state == "response":
        update_progress_bar()

        # wait 4 seconds, then change state
        if pygame.time.get_ticks() / 1000 - timer > 10:
            change_state("question")
            screen.fill(BG_COLOR)
            main_question()
            pygame.display.flip()
            
    # Limit the frame rate
    clock.tick(FPS)

pygame.quit()
