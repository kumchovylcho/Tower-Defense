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
    draw_gradient.draw_gradient(
        screen,
        GRADIENT_START,
        GRADIENT_END,
        config["Display"]["GRADIENT_DIRECTION"].lower()
    )


field_config = {
    "obstacle_positions": (),
    "obstacle_images": [
        pg.transform.scale(
            pg.image.load("assets/blocks/wood_on_grass.png").convert_alpha(),
            (constants.TILE_SIZE, constants.TILE_SIZE)
        )
    ],
    "path_tile": pg.transform.scale(
        pg.image.load("assets/blocks/stone.png").convert_alpha(),
        (constants.TILE_SIZE, constants.TILE_SIZE)
    ),
    "buildable_tile": pg.transform.scale(
        pg.image.load("assets/blocks/grass_2.png").convert_alpha(),
        (constants.TILE_SIZE, constants.TILE_SIZE)
    ),
    "hover_color_on_tiles": (255, 255, 0, 128)
}
field = Field(
    (
    (20, 0), (20, 8), (6, 8), (6, 16), (15, 16), (20, 22), (30, 32)
    ),
    (constants.FIELD_ROWS, constants.FIELD_COLS, constants.TILE_SIZE),
    (WIDTH, HEIGHT),
    field_config,
)
field.create_field()


# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    # fill background with some color if the user wants so
    if not IS_GRADIENT_BACKGROUND:
        screen.fill(REGULAR_BACKGROUND_COLOR)

    field.render_tiles(screen)


    # Update display
    pg.display.flip()
    clock.tick(constants.FPS)

pg.quit()