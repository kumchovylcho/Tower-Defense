import pygame as pg


class Button:
    def __init__(self,
                 position: tuple[int, int],
                 normal_image_path: pg.Surface,
                 hover_image_path: pg.Surface,
                 shadow_offset=None,
                 shadow_color=None,
                 on_hover_cursor=None,
                 ):
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

        :param on_hover_cursor: a cursor from `pg.constants`
            Reference: https://www.pygame.org/docs/ref/cursors.html
        """

        self.x, self.y = position
        self.normal_image = normal_image_path
        self.button_rect = self.normal_image.get_rect(topleft=position)
        self.button_mask = pg.mask.from_surface(self.normal_image)

        self.hover_image = hover_image_path

        self.width, self.height = self.normal_image.get_size()

        # shadow settings
        self.shadow_offset = shadow_offset
        self.shadow_color = shadow_color
        self.shadow_surface = None
        if self.shadow_offset and self.shadow_color:
            self.shadow_surface = self._create_shadow()

        # cursor settings
        self.on_hover_cursor = on_hover_cursor
        self.is_cursor_changed = False


    def _create_shadow(self) -> pg.Surface:
        """
        pre-renders the shadow effect based on the current shadow settings.
        """

        shadow_mask = pg.mask.from_surface(self.normal_image)
        shadow_surface = pg.Surface((self.width, self.height), flags=pg.SRCALPHA)
        shadow_surface.fill((0, 0, 0, 0))

        shadow_mask_surface = shadow_mask.to_surface(setcolor=self.shadow_color, unsetcolor=(0, 0, 0, 0))
        shadow_surface.blit(shadow_mask_surface, (0, 0))

        return shadow_surface

    def is_hover(self) -> bool:
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

    def _update_cursor(self, is_hovered: bool) -> None:
        """
        Updates the cursor based on whether the button is hovered.
        """
        if not self.on_hover_cursor:
            return

        if is_hovered:
            if not self.is_cursor_changed:
                pg.mouse.set_cursor(self.on_hover_cursor)
                self.is_cursor_changed = True
        else:
            if self.is_cursor_changed:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                self.is_cursor_changed = False

    def render(self, screen: pg.Surface) -> None:
        """
        Draws the button and its shadow on the screen.

        :param screen: The pygame Surface to draw on.
        """
        # draw shadow
        if self.shadow_surface:
            shadow_pos = (self.x + self.shadow_offset[0], self.y + self.shadow_offset[1])
            screen.blit(self.shadow_surface, shadow_pos)


        is_hovered = self.is_hover()
        # draw button (normal or hover)
        image_to_display = self.hover_image if is_hovered else self.normal_image
        screen.blit(image_to_display, (self.x, self.y))

        # updates the cursor from self.on_hover_cursor back to its default(arrow)
        self._update_cursor(is_hovered)
