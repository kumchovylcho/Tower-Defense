import pygame as pg
import configparser

from utils import draw_gradient
import constants
from field.tile import Tile
from field.field import Field


# load user settings
config = configparser.ConfigParser()
config.read("CONFIG.cfg")


# Initialize Pygame
pg.init()

# Clock for capping FPS
clock = pg.time.Clock()


# Screen settings
WIDTH, HEIGHT = int(config["Display"]["WIDTH"]), int(config["Display"]["HEIGHT"])
IS_GRADIENT_BACKGROUND = bool(int(config["Display"]["GRADIENT"]))
REGULAR_BACKGROUND_COLOR = [int(color) for color in config["Display"]["BACKGROUND_COLOR"].split(", ")]
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tower-Defense")
if IS_GRADIENT_BACKGROUND:
    GRADIENT_START = [int(color) for color in config["Display"]["GRADIENT_START"].split(", ")]
    GRADIENT_END = [int(color) for color in config["Display"]["GRADIENT_END"].split(", ")]




matrix_size = 700
matrix_surface = pg.Surface((matrix_size, matrix_size))
GRID_ROWS = matrix_surface.get_width() // constants.TILE_SIZE
GRID_COLS = matrix_surface.get_height() // constants.TILE_SIZE
# Prepare tile settings
HOVER_COLOR = (255, 255, 0, 128)  # Yellow with transparency
# load tile
scaled_image = pg.transform.scale(
    pg.image.load("assets/blocks/grass_2.png").convert_alpha(),
    (constants.TILE_SIZE, constants.TILE_SIZE)
)


field = Field([
    [
        Tile(
            image=scaled_image,
            position=(col * constants.TILE_SIZE, row * constants.TILE_SIZE),
            hover_color=HOVER_COLOR,
        )
        for col in range(GRID_COLS)
    ]
    for row in range(GRID_ROWS)
    ]
)



# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    # fill background with some color if the user wants so
    if not IS_GRADIENT_BACKGROUND:
        screen.fill(REGULAR_BACKGROUND_COLOR)
    else:
        draw_gradient.draw_gradient(
            screen,
            GRADIENT_START,
            GRADIENT_END,
            config["Display"]["GRADIENT_DIRECTION"].lower()
        )

    field.render_tiles(screen)


    # Update display
    pg.display.flip()
    clock.tick(constants.FPS)

pg.quit()