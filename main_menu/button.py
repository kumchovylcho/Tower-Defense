import pygame as pg


class Button:
    def __init__(self,
                 position: tuple,
                 normal_image_path: pg.Surface,
                 hover_image_path: pg.Surface):
        """
        Initializes the button with specific images for normal and hover states.

        :param position: Tuple (x, y) for the top-left corner of the button.
        :param normal_image_path: File path for the button's normal state image.
        :param hover_image_path: File path for the button's hover state image.
        """

        self.x, self.y = position
        self.normal_image = normal_image_path
        self.button_rect = self.normal_image.get_rect(topleft=position)
        self.button_mask = pg.mask.from_surface(self.normal_image)

        self.hover_image = hover_image_path
        self.hover_rect = self.hover_image.get_rect(topleft=position)

        # self.callback = callback
        # self.is_hovered = False

        # Get the button's size from the image dimensions
        self.width, self.height = self.normal_image.get_size()

    def render(self, screen: pg.Surface):
        """
        Draws the button on the screen.

        :param screen: The pygame Surface to draw on.
        """
        if self.is_hover():
            screen.blit(self.hover_image, (self.x, self.y))
        else:
            screen.blit(self.normal_image, (self.x, self.y))

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


    def handle_event(self, event: pg.event.Event):
        """
        Handles mouse events for the button.

        :param event: A Pygame event (e.g., MOUSE MOTION or SEMIAUTONOMOUS).
        """
        if event.type == pg.MOUSEMOTION:
            self.is_hover()


