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
        self.image_rect = image.get_rect()
        self.x_pos, self.y_pos, = position
        self.overlay = self.prepare_regular_hover_overlay(hover_color, self.image_rect.size)

        if border_roundings:
            self.border_roundings = border_roundings
            self.rounded_image, self.rounded_mask_surface = self.apply_border_radius(**border_roundings)

            # pixel perfect mask needed for mouse collisions
            self.rounded_mask = pg.mask.from_surface(self.rounded_mask_surface)
            # needed to check if it's close enough, so we can check for the mask collision.
            # this is needed so it requires less resources
            self.rounded_image_rect = self.rounded_image.get_rect(topleft=(self.x_pos, self.y_pos))
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

    def apply_border_radius(self, **roundings):
        # Create a rounded mask
        rounded_mask = pg.Surface(self.image_rect.size, pg.SRCALPHA)
        pg.draw.rect(rounded_mask, (255, 255, 255, 255), self.image_rect, **roundings)

        # Create a new surface for the result
        rounded_image = pg.Surface(self.image_rect.size, pg.SRCALPHA)
        rounded_image.blit(self.image, (0, 0))  # Draw the image
        rounded_image.blit(rounded_mask, (0, 0), special_flags=pg.BLEND_RGBA_MIN)  # Apply mask

        return rounded_image, rounded_mask

    def create_masked_hover_overlay(self, size: tuple, hover_color: tuple, mask: pg.Mask):
        # create a transparent overlay
        self.prepare_regular_hover_overlay(hover_color, size)

        # apply mask directly
        mask_surface = mask.to_surface(setcolor=hover_color, unsetcolor=(0, 0, 0, 0))
        masked_overlay = pg.Surface(size, pg.SRCALPHA)
        masked_overlay.blit(mask_surface, (0, 0))

        return masked_overlay

    def mouse_collides_with_block(self):
        mouse_pos = pg.mouse.get_pos()
        # means we are far away from the block
        if not self.image_rect.collidepoint(mouse_pos):
            return False

        # now we are very close to the block or right above it
        relative_mouse_pos = (
            mouse_pos[0] - self.image_rect.x,
            mouse_pos[1] - self.image_rect.y
        )
        # check for perfect pixel collision
        if not self.rounded_mask.get_at(relative_mouse_pos):
            return False
        return True

    def render_block(self, surface: pg.Surface):
        has_roundings = hasattr(self, "border_roundings")
        image_to_show = self.rounded_image if has_roundings else self.image
        surface.blit(image_to_show, self.image_rect.topleft)

        if self.mouse_collides_with_block():
            get_image_rect_for_overlay = self.image_rect if has_roundings else self.rounded_image_rect
            surface.blit(self.overlay, get_image_rect_for_overlay.topleft)
