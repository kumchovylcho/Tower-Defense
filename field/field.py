import pygame as pg

from .tile import Tile


class Field:
    def __init__(self, field_dimensions: tuple, screen_dimensions: tuple):
        """
        :param field_dimensions: (rows, cols, tile_size)
        :param screen_dimensions: (screen_width, screen_height) - needed for centering the field
        """
        self.field: [Tile] = []
        self.rows, self.cols, self.tile_size = field_dimensions
        self.field_width = self.cols * self.tile_size
        self.field_height = self.rows * self.tile_size
        self.x_offset, self.y_offset = self.get_centering_offset(screen_dimensions)

        self.static_surface = None

    def get_centering_offset(self, screen_dimensions: tuple) -> tuple:
        screen_width, screen_height = screen_dimensions
        x_offset = (screen_width - self.field_width) // 2
        y_offset = (screen_height - self.field_height) // 2
        return x_offset, y_offset

    def create_static_surface(self):
        if not self.field:
            raise ValueError("Field must be created first.")

        self.static_surface = pg.Surface((self.field_width + self.x_offset,
                                     self.field_height + self.y_offset),
                                    pg.SRCALPHA)
        self.static_surface.fill((0, 0, 0, 0))
        for row in self.field:
            for tile in row:
                self.static_surface.blit(tile.image, tile.image_rect.topleft)

    def create_field(self, field: list[list[int]]):
        """
        must create the field in the future.
        """
        pass

    def render_tiles(self, surface_to_draw_on: pg.Surface):
        surface_to_draw_on.blit(self.static_surface, (0, 0))
        for row in self.field:
            for tile in row:

                tile.render_block(surface_to_draw_on)
