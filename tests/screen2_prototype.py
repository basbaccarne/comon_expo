# This is the visual design for screen 2

# modules
import pygame
from pathlib import Path
import time
import os

# Initialize Pygame
pygame.init()

# FPS (PyGame)
FPS = 30

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
GREEN_TOP = IMG_DIR / 'top_green.png'
GREEN_BOTTOM = IMG_DIR / 'bottom_green.png'
RED_TOP = IMG_DIR / 'top_red.png'
RED_BOTTOM = IMG_DIR / 'bottom_red.png'
YELLOW_TOP = IMG_DIR / 'top_yellow.png'
YELLOW_BOTTOM = IMG_DIR / 'bottom_yellow.png'
AKKOORD_2 = IMG_DIR / 'akkoord_2.png'
NIETAKKOORD_2 = IMG_DIR / 'nietakkoord_2.png'
GEENMENING_2 = IMG_DIR / 'geenmening_2.png'

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
pygame.mouse.set_visible(False)

# GLOBAL VARIABLES
"""timer"""
bar_height = 40
bar_width = SCREEN_WIDTH
bar_area = pygame.Rect(SCREEN_WIDTH - bar_height, 0,  bar_height, bar_width)
bin_width = 0
start_time = 0

# FUNCTIONAL FUNCTIONS
def load_votes():
    """Load previous votes if available"""
    return {"button1": 20, "button2": 30, "button3": 50}

def init_Progress_bar(time_duration):
    """Initialize the progress bar with the given duration."""
    global bin_width, start_time, duration

    # Draw the initial progress bar
    pygame.draw.rect(screen, DARKBLUE, bar_area)
    
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
    
def response_screen():
    """Display the response screen (static)"""
    global votes, pressed

    # background
    screen.fill(BG_COLOR)

    # text scene 2 (dit is wat andere gentenaars denken)
    text_position1 = (150, SCREEN_HEIGHT // 2)
    text_position2 = (250, SCREEN_HEIGHT // 2)
    line1 = FONT.render("Dit is wat andere", True, DARKBLUE)
    line2 = FONT.render("Gentenaars denken", True, DARKBLUE)
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

    # load progress bar
    init_Progress_bar(20)

    # render
    pygame.display.flip()


# PRELOADING #
##############

# Load JSON file with from previous sessions
votes = load_votes()
print("Current votes:", votes)

# Preload images
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
geenmening_2 = pygame.image.load(GEENMENING_2).convert_alpha()
geenmening_2 = pygame.transform.rotate(geenmening_2, 90)
nietakkoord_2 = pygame.image.load(NIETAKKOORD_2).convert_alpha()
nietakkoord_2 = pygame.transform.rotate(nietakkoord_2, 90)

# Preload first screen
response_screen()

# MAIN GAME LOOP #
##################

clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
running = True

while running:

    # Exit the progam on ctrl + C
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # STATE MACHINE #
    #################

    # STATE: QUESTION

    # STATE: RESPONSE_ANIMATION
    
    # STATE: RESPONSE SCREEN
    # Update the progress bar
    update_progress_bar()

    # Limit the frame rate
    clock.tick(FPS)

pygame.quit()
