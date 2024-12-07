import pygame as pg


class Tile:
    def __init__(self, image: pg.Surface, position: tuple, hover_color: tuple, is_path_or_obstacle=False):
        """
        :param image: loaded and already scaled image
        :param position: (x_pos, y_pos)
        :param hover_color: (R, G, B, alpha(0 to 255)) alpha means that it needs a value from 0 to 255 raw number
        :param is_path_or_obstacle: If the tile is obstacle or not
        """
        self.image = image
        self.image_rect = image.get_rect(topleft=position)
        self.overlay = pg.Surface(self.image_rect.size, pg.SRCALPHA)
        self.overlay.fill(hover_color)

        self.is_path_or_obstacle = is_path_or_obstacle

    def mouse_collides_with_block(self):
        mouse_pos = pg.mouse.get_pos()
        # means we are far away from the block
        if not self.image_rect.collidepoint(mouse_pos):
            return False
        return True

    def render_block(self, surface_to_draw_on: pg.Surface):
        surface_to_draw_on.blit(self.image, self.image_rect.topleft)
        if self.mouse_collides_with_block():
            surface_to_draw_on.blit(self.overlay, self.image_rect.topleft)