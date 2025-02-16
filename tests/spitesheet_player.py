import pygame
import os

# Initialize pygame
pygame.init()

# Configuration
FPS = 25  # Adjust speed of animation
IMAGE_FOLDER = "tests/img"  # Folder containing PNGs
SCREEN_SIZE = (800, 800)  # Window size
RESCALE_VIDEO = (400,400)

# Load images
images = []
for file in sorted(os.listdir(IMAGE_FOLDER)):
    if file.endswith(".png"):
        img = pygame.image.load(os.path.join(IMAGE_FOLDER, file))
        images.append(img)

if not images:
    raise ValueError("No PNG images found in the specified folder.")

# Resize images to fit screen
images = [pygame.transform.scale(img, RESCALE) for img in images]
center = ((SCREEN_SIZE[0] // 2) - (RESCALE[0]//2), (SCREEN_SIZE[1] // 2) - (RESCALE[1]//2))

# Set up display
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("PNG Animation Player")
clock = pygame.time.Clock()

# Animation loop
running = True
frame = 0
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display current frame
    screen.blit(images[frame], center)
    pygame.display.update()
    
    # Update frame
    frame = (frame + 1) % len(images)

pygame.quit()
