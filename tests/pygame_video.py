# In this test I want to integreate a lottie animation in a pygame window
# 1. Create and modify an animation on the lottiefiles website
# 2. Get the embed URL
# 3. Embed the animation in a HTML file (see example in /lottieHTML) & change the parameters
# 4. Launch the HTML page
# 5. Capture the animation with the browser & OBS

# modules
import pygame
import pygvideo

# init
pygame.init()
running = True

# load video
video = pygvideo.Video('tests/lottieHTML/animation.mkv')

# set up screen
screen = pygame.display.set_mode((800, 800))

# control FR
clock = pygame.time.Clock()

# adjusts the video size to match the window size.
video.set_size(screen.get_size())

# prepare the video for playback.
video.preplay(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        video.handle_event(event)

    # draw the video to the screen
    video.draw_and_update(screen, (0, 0))

    # update the display
    pygame.display.flip()

    # control the frame rate
    clock.tick(video.get_fps())

pygvideo.quit_all()
pygame.quit()