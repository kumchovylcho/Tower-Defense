import pygame as pg


class Tile:
    def __init__(self, image: pg.Surface, position: tuple, hover_color: tuple, **border_roundings):
        """
        :param image: loaded and already scaled image
        :param position: (x_pos, y_pos)
        :param hover_color: (R, G, B, alpha(0 to 255)) alpha means that it needs a value from 0 to 255 raw number
        :param border_roundings:
             border_radius=5 rounds all edges by 5px,
             border_top_left_radius,
             border_top_right_radius,
             border_bottom_left_radius,
             border_bottom_right_radius
        """
        self.image = image
        self.image_rect = image.get_rect(topleft=position)
        self.overlay = self.prepare_regular_hover_overlay(hover_color, self.image_rect.size)
        self.has_roundings = len(border_roundings) > 0

        if self.has_roundings:
            self.rounded_image, self.rounded_mask_surface = self.apply_border_radius(**border_roundings)

            # pixel perfect mask needed for mouse collisions
            self.rounded_mask = pg.mask.from_surface(self.rounded_mask_surface)
            # needed to check if it's close enough, so we can check for the mask collision.
            # this is needed so it requires less resources
            self.rounded_image_rect = self.rounded_image.get_rect(topleft=position)
            self.overlay = self.create_masked_hover_overlay(self.rounded_image.get_size(),
                                                            hover_color,
                                                            self.rounded_mask
                                                            )

    @staticmethod
    def prepare_regular_hover_overlay(hover_color: tuple, size: tuple):
        # create a transparent overlay
        overlay = pg.Surface(size, pg.SRCALPHA)
        overlay.fill(hover_color)

        return overlay

    @staticmethod
    def create_masked_hover_overlay(size: tuple, hover_color: tuple, mask: pg.Mask):
        # apply mask directly
        mask_surface = mask.to_surface(setcolor=hover_color, unsetcolor=(0, 0, 0, 0))
        masked_overlay = pg.Surface(size, pg.SRCALPHA)
        masked_overlay.blit(mask_surface, (0, 0))

        return masked_overlay

    def apply_border_radius(self, **roundings):
        # rounded mask with transparent background
        rounded_mask = pg.Surface(self.image_rect.size, pg.SRCALPHA)
        # transparent
        rounded_mask.fill((0, 0, 0, 0))

        # draw the rounded rect
        pg.draw.rect(
            rounded_mask,
            (255, 255, 255, 255), # transparent
            (0, 0, self.image_rect.width, self.image_rect.height),
            **roundings
        )

        # new surface for the rounded image
        rounded_image = pg.Surface(self.image_rect.size, pg.SRCALPHA)
        # make it transparent
        rounded_image.fill((0, 0, 0, 0))

        # keep only the visible parts of the image and apply the mask
        rounded_image.blit(self.image, (0, 0))
        rounded_image.blit(rounded_mask, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

        return rounded_image, rounded_mask

    def mouse_collides_with_block(self):
        mouse_pos = pg.mouse.get_pos()
        # means we are far away from the block
        if not self.image_rect.collidepoint(mouse_pos):
            return False

        # means that we are right above the block and the edges are not rounded,
        # so we don't need to do the expensive calculations for the mask. We return True
        # since we are not dealing with any masks here
        if not self.has_roundings:
            return True

        relative_mouse_pos = (
            mouse_pos[0] - self.image_rect.x,
            mouse_pos[1] - self.image_rect.y
        )
        # now we are very close to the block or right above it and the block has rounded edges
        # check for perfect pixel collision
        if not self.rounded_mask.get_at(relative_mouse_pos):
            return False
        return True

    def render_block(self, surface: pg.Surface):
        image_to_show = self.rounded_image if self.has_roundings else self.image
        surface.blit(image_to_show, self.image_rect.topleft)

        if self.mouse_collides_with_block():
            surface.blit(self.overlay, self.image_rect.topleft)
