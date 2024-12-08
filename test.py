import pygame as pg
import configparser

from main_menu.button import Button
from utils import draw_gradient

# Read configuration file
config = configparser.ConfigParser()
config.read("CONFIG.cfg")

# Initialize Pygame
pg.init()
pg.font.init()

# Clock setup
clock = pg.time.Clock()

# Screen dimensions and settings
WIDTH, HEIGHT = int(config["Display"]["WIDTH"]), int(config["Display"]["HEIGHT"])
IS_GRADIENT_BACKGROUND = bool(int(config["Display"]["GRADIENT"]))
REGULAR_BACKGROUND_COLOR = [
    int(color) for color in config["Display"]["BACKGROUND_COLOR"].split(", ")
]

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tower-Defense")

# Gradient background colors
if IS_GRADIENT_BACKGROUND:
    GRADIENT_START = [
        int(color) for color in config["Display"]["GRADIENT_START"].split(", ")
    ]
    GRADIENT_END = [
        int(color) for color in config["Display"]["GRADIENT_END"].split(", ")
    ]

# Load assets
background_menu = pg.transform.scale(
    pg.image.load("assets/main_menu_images/background_menu_images/menu_background.jpg"),
    (400, 500),
)

# Correctly initialize buttons
button1 = Button(
    (650, 400),
    pg.transform.scale(
        pg.image.load("assets/main_menu_images/buttons/back_button_1.png").convert_alpha(),
        (300, 80),
    ),
    pg.transform.scale(
        pg.image.load("assets/main_menu_images/buttons/back_button_2.png").convert_alpha(),
        (300, 75),
    ),
    (5, 5),
    (0, 0, 0, 100)
)

button2 = Button(
    (650, 480),
    pg.transform.scale(
        pg.image.load("assets/main_menu_images/buttons/exit_button_1.png").convert_alpha(),
        (300, 80),
    ),
    pg.transform.scale(
        pg.image.load("assets/main_menu_images/buttons/exit_button_2.png").convert_alpha(),
        (300, 75),
    ),
    (5, 5),
    (0, 0, 0, 100)
)

button3 = Button(
    (650, 320),
    pg.transform.scale(
        pg.image.load("assets/main_menu_images/buttons/shop_button_1.png").convert_alpha(),
        (300, 80),
    ),
    pg.transform.scale(
        pg.image.load("assets/main_menu_images/buttons/shop_button_2.png").convert_alpha(),
        (300, 75),
    ),
    (5, 5),
    (0, 0, 0, 100)
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

    # Draw the background
    if not IS_GRADIENT_BACKGROUND:
        screen.fill(REGULAR_BACKGROUND_COLOR)
    else:
        draw_gradient.draw_gradient(
            screen,
            GRADIENT_START,
            GRADIENT_END,
            config["Display"]["GRADIENT_DIRECTION"].lower(),
        )

    # Draw menu background
    screen.blit(background_menu, (600, 200))

    # Render buttons
    for button in buttons:
        button.render(screen)

    # Update display
    pg.display.flip()

# Quit Pygame
pg.quit()
