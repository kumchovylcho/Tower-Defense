import pygame as pg
import configparser

from ui.button import Button
from game import constants

# Read configuration file
config = configparser.ConfigParser()
config.read("CONFIG.cfg")

# Initialize Pygame
pg.init()
pg.font.init()

# Clock setup
clock = pg.time.Clock()

# Screen dimensions and settings
WIDTH, HEIGHT = constants.DIMENSIONS

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tower-Defense")


# Load assets
background_menu = pg.transform.scale(
    pg.image.load("assets/menu_images/initial_menu/background_menu/menu_background.png"),
    (400, 500),
)

# Correctly initialize buttons
button1 = Button(
    (650, 400),
    pg.transform.scale(
        pg.image.load("assets/menu_images/initial_menu/buttons/back_button_1.png").convert_alpha(),
        (300, 80),
    ),
    pg.transform.scale(
        pg.image.load("assets/menu_images/initial_menu/buttons/back_button_2.png").convert_alpha(),
        (300, 75),
    ),
    (5, 5),
    (0, 0, 0, 100),
    pg.SYSTEM_CURSOR_HAND
)

button2 = Button(
    (650, 480),
    pg.transform.scale(
        pg.image.load("assets/menu_images/initial_menu/buttons/exit_button_1.png").convert_alpha(),
        (300, 80),
    ),
    pg.transform.scale(
        pg.image.load("assets/menu_images/initial_menu/buttons/exit_button_2.png").convert_alpha(),
        (300, 75),
    ),
    (5, 5),
    (0, 0, 0, 100),
    pg.SYSTEM_CURSOR_CROSSHAIR
)

button3 = Button(
    (650, 320),
    pg.transform.scale(
        pg.image.load("assets/menu_images/initial_menu/buttons/shop_button_1.png").convert_alpha(),
        (300, 80),
    ),
    pg.transform.scale(
        pg.image.load("assets/menu_images/initial_menu/buttons/shop_button_2.png").convert_alpha(),
        (300, 75),
    ),
    (5, 5),
    (0, 0, 0, 100),
    pg.SYSTEM_CURSOR_WAIT
)


buttons = [button1, button2, button3]

# Main game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # Uncomment if button events are handled
        # for button in buttons:
        #     button.handle_event(event)


    # Draw menu background
    screen.blit(background_menu, (600, 200))

    # Render buttons
    for button in buttons:
        button.render(screen)

    # Update display
    pg.display.flip()

# Quit Pygame
pg.quit()
