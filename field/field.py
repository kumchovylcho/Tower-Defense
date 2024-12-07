import pygame as pg

from .tile import Tile


class Field:
    def __init__(self, field: [Tile]):
        self.field = field

    def render_tiles(self, surface_to_draw_on: pg.Surface):
        for row in range(len(self.field)):
            for col in range(len(self.field[row])):
                tile = self.field[row][col]
                tile.render_block(surface_to_draw_on)
