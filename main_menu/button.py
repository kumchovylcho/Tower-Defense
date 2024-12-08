import pygame as pg


class Button:
    def __init__(self,
                 position: tuple,
                 normal_image_path: pg.Surface,
                 hover_image_path: pg.Surface,
                 shadow_offset=None,  # Default shadow offset
                 shadow_color=None,
                 is_shadow_effect=True):  # Default shadow color
        """
        Initializes the button with specific images for normal and hover states.

        :param position: Tuple (x, y) for the top-left corner of the button.
        :param normal_image_path: File path for the button's normal state image.
        :param hover_image_path: File path for the button's hover state image.

        :param shadow_offset:
            - optional(None)
            if you want to create a shadow effect provide.
                - tuple(int, int, int, int)

        :param shadow_color:
            - optional(None)
            - if you want to create a shadow effect provide.
                - tuple(int, int, int, int)

        :param is_shadow_effect:
            - optional(True)
            if you want to deactivate it, set it to False:
            Otherwise provide shadow offset and shadow color

        """
        self.x, self.y = position
        self.normal_image = normal_image_path
        self.button_rect = self.normal_image.get_rect(topleft=position)
        self.button_mask = pg.mask.from_surface(self.normal_image)

        self.hover_image = hover_image_path
        self.hover_rect = self.hover_image.get_rect(topleft=position)

        self.width, self.height = self.normal_image.get_size()

        # Shadow settings
        self.shadow_offset = shadow_offset
        self.shadow_color = shadow_color
        self.is_shadow_effect = is_shadow_effect

        # Create shadow surface
        self.shadow = pg.Surface(self.normal_image.get_size(), flags=pg.SRCALPHA)

    def shadow_effect(self, screen: pg.Surface):
        shadow_mask = pg.mask.from_surface(self.normal_image)

        if self.shadow_offset and self.shadow_color:
            # Fill the shadow surface with transparency
            self.shadow.fill((0, 0, 0, 0))

            # Generate a surface from the mask
            shadow_surface = shadow_mask.to_surface(setcolor=self.shadow_color, unsetcolor=(0, 0, 0, 0))

            self.shadow.blit(shadow_surface, (0, 0))

            shadow_pos = (self.x + self.shadow_offset[0], self.y + self.shadow_offset[1])
            screen.blit(self.shadow, shadow_pos)

    def is_hover(self):
        """
        Updates hover state based on the mouse position.
        """
        mouse_x, mouse_y = pg.mouse.get_pos()
        relative_mouse_pos = (mouse_x - self.button_rect.x, mouse_y - self.button_rect.y)
        if (0 <= relative_mouse_pos[0] < self.button_rect.width and
                0 <= relative_mouse_pos[1] < self.button_rect.height):
            if self.button_mask.get_at(relative_mouse_pos):  # Pixel-perfect check
                return True
        return False

    def render(self, screen: pg.Surface):
        """
        Draws the button and its shadow on the screen.

        :param screen: The pygame Surface to draw on.
        """
        # Draw shadow
        if self.is_shadow_effect:
            self.shadow_effect(screen)

        # Draw button (normal or hover)
        if self.is_hover():
            screen.blit(self.hover_image, (self.x, self.y))
        else:
            screen.blit(self.normal_image, (self.x, self.y))

