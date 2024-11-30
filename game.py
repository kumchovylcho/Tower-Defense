import pygame
import configparser

import utils

# load user settings
config = configparser.ConfigParser()
config.read("CONFIG.cfg")


# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = int(config["Display"]["WIDTH"]), int(config["Display"]["HEIGHT"])
IS_GRADIENT_BACKGROUND = bool(int(config["Display"]["GRADIENT"]))
REGULAR_BACKGROUND_COLOR = [int(color) for color in config["Display"]["BACKGROUND_COLOR"].split(", ")]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower-Defense")

if IS_GRADIENT_BACKGROUND:
    utils.draw_gradient(
        screen,
        [int(color) for color in config["Display"]["GRADIENT_START"].split(", ")],
        [int(color) for color in config["Display"]["GRADIENT_END"].split(", ")],
        config["Display"]["GRADIENT_DIRECTION"].lower()
    )

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill background with some color if the user wants so
    if not IS_GRADIENT_BACKGROUND:
        screen.fill(REGULAR_BACKGROUND_COLOR)



    # Update display
    pygame.display.flip()

pygame.quit()
