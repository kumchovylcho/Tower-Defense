import pygame as pg
import configparser

from game import constants
from field.field import Field
from main_menu.utils import load_image_from_assets


class Game:
    def __init__(self):
        self.running = True
        self.screen = pg.display.set_mode(constants.DIMENSIONS)
        pg.display.set_caption(constants.WINDOW_NAME)
        self.clock = pg.time.Clock()

        # load settings
        config = configparser.ConfigParser()
        config.read("CONFIG.cfg")

        # create map
        field_config = {
            "obstacle_positions": (),
            "obstacle_images": [
                pg.transform.scale(
                    load_image_from_assets(constants.WOOD_ON_GRASS_BLOCK),
                    (constants.TILE_SIZE, constants.TILE_SIZE)
                )
            ],
            "path_tile": pg.transform.scale(
                load_image_from_assets(constants.STONE_BLOCK),
                (constants.TILE_SIZE, constants.TILE_SIZE)
            ),
            "path_width": 3,
            "buildable_tile": pg.transform.scale(
                load_image_from_assets(constants.GRASS_2_BLOCK),
                (constants.TILE_SIZE, constants.TILE_SIZE)
            ),
            "hover_color_on_tiles": (255, 255, 0, 128)
        }
        self.field = Field(
            (
                (20, 0), (20, 8), (6, 8), (6, 16), (15, 16), (20, 22), (31, 32)
            ),
            (constants.FIELD_ROWS, constants.FIELD_COLS, constants.TILE_SIZE),
            constants.DIMENSIONS,
            field_config,
        )
        self.field.create_field()

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))

            self.field.render_tiles(self.screen)

            # Update display
            pg.display.flip()
            self.clock.tick(constants.FPS)

        pg.quit()
