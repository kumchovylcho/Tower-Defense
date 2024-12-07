import pygame as pg
import configparser

from main_menu.button import Button
from utils import draw_gradient

config = configparser.ConfigParser()
config.read("CONFIG.cfg")

clock = pg.time.Clock()

WIDTH, HEIGHT = int(config["Display"]["WIDTH"]), int(config["Display"]["HEIGHT"])
IS_GRADIENT_BACKGROUND = bool(int(config["Display"]["GRADIENT"]))
REGULAR_BACKGROUND_COLOR = [int(color) for color in config["Display"]["BACKGROUND_COLOR"].split(", ")]
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tower-Defense")
if IS_GRADIENT_BACKGROUND:
    GRADIENT_START = [int(color) for color in config["Display"]["GRADIENT_START"].split(", ")]
    GRADIENT_END = [int(color) for color in config["Display"]["GRADIENT_END"].split(", ")]

pg.init()
pg.font.init()

background_menu = pg.transform.scale(pg.image.load("assets/buttons/menu_background.jpg"), (400, 400))

button = Button((650, 400),
                pg.transform.scale(pg.image.load("assets/buttons/back_button_1.png").convert_alpha(), (300, 100)),
                pg.transform.scale(pg.image.load("assets/buttons/back_button_2.png").convert_alpha(), (300, 100)
                                   ))

button2 = Button((650, 480),
                 pg.transform.scale(pg.image.load("assets/buttons/exit_button_1.png").convert_alpha(), (300, 100)),
                 pg.transform.scale(pg.image.load("assets/buttons/exit_button_2.png").convert_alpha(), (300, 100)
                                    ))

buttons = [button, button2]

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # button.handle_event(event)

    if not IS_GRADIENT_BACKGROUND:
        screen.fill(REGULAR_BACKGROUND_COLOR)
    else:
        draw_gradient.draw_gradient(
            screen,
            GRADIENT_START,
            GRADIENT_END,
            config["Display"]["GRADIENT_DIRECTION"].lower()
        )

    # draw menu background on the screen
    screen.blit(background_menu, (600, 300))
    # Render button
    for button in buttons:
        button.render(screen)

    # Update display
    pg.display.flip()

# Quit Pygame
pg.quit()
