import pygame as pg


class HorizontalVolumeScrollbar:
    def __init__(self,
                 screen: pg.Surface,
                 scrollbar_dimensions: tuple[int, int, int, int],
                 scrollbar_color: tuple[int, int, int],
                 knob_dimensions: tuple[int, int],
                 knob_color: tuple[int, int, int],
                 scrollbar_border_radii=None,
                 knob_border_radii=None,
                 initial_volume=0.5):
        """
        screen: The Pygame surface to draw on.
        scrollbar_dimensions: The dimensions of the scrollbar (x, y, w, h).
        scrollbar_color: tuple of rgb values (r, g, b).
        knob_dimensions: Dimensions of the knob (w, h).
        knob_color: tuple of rgb values (r, g, b).
        scrollbar_border_radii: dictionary with border radius for the drawing. Can be multiple border radii.
        knob_border_radii: dictionary with border radius for the drawing. Can be multiple border radii.
        initial_volume: Initial volume level (0.0 to 1.0) 0 for 0% and 1 for 100%.
        """
        self.screen = screen
        self.scrollbar_x = scrollbar_dimensions[0]
        self.scrollbar_y = scrollbar_dimensions[1]
        self.scrollbar_width = scrollbar_dimensions[2]
        self.scrollbar_height = scrollbar_dimensions[3]
        self.scrollbar_color = scrollbar_color
        self.scrollbar_border_radii = {}
        if scrollbar_border_radii is not None:
            self.scrollbar_border_radii = scrollbar_border_radii

        self.knob_width = knob_dimensions[0]
        self.knob_height = knob_dimensions[1]
        self.knob_color = knob_color
        self.knob_border_radii = {}
        if knob_border_radii is not None:
            self.knob_border_radii = knob_border_radii

        self.previous_volume = initial_volume
        self.volume = initial_volume
        # if the knob is being dragged
        self.dragging = False
        # offset to center the knob on the mouse
        self.offset_x = 0

        # Initialize the knob rectangle
        self.knob_rect = self._create_knob_rect()

    def _create_knob_rect(self) -> pg.Rect:
        # initial X position of the knob
        knob_x = self.scrollbar_x + int(self.volume * (self.scrollbar_width - self.knob_width))
        knob_y = self.scrollbar_y - (self.knob_height - self.scrollbar_height) // 2
        return pg.Rect(knob_x, knob_y, self.knob_width, self.knob_height)

    def _update_knob_position(self) -> None:
        self.knob_rect.x = self.scrollbar_x + int(self.volume * (self.scrollbar_width - self.knob_width))

    def _is_clicked_inside_scrollbar(self, mouse_pos: tuple[int, int]) -> bool:
        return (
                self.scrollbar_x <= mouse_pos[0] <= self.scrollbar_x + self.scrollbar_width and
                self.scrollbar_y <= mouse_pos[1] <= self.scrollbar_y + self.scrollbar_height
        )

    def draw(self):
        """
        draw the scrollbar and knob on the screen.
        """
        # draw the scrollbar
        pg.draw.rect(self.screen,
                     self.scrollbar_color,
                     (self.scrollbar_x, self.scrollbar_y, self.scrollbar_width, self.scrollbar_height),
                     **self.scrollbar_border_radii
                     )
        # draw the knob
        pg.draw.rect(self.screen, self.knob_color, self.knob_rect, **self.knob_border_radii)

    def has_volume_changed(self) -> bool:
        if self.volume != self.previous_volume:
            self.previous_volume = self.volume
            return True
        return False

    def handle_event(self, event: pg.event) -> None:
        """
        handles mouse events to update the scrollbar's state.
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True
                # center the knob on the mouse
                self.offset_x = event.pos[0] - self.knob_rect.x
            elif self._is_clicked_inside_scrollbar(event.pos):
                self.update_volume(event.pos[0])
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pg.MOUSEMOTION and self.dragging:
            self.update_volume(event.pos[0] - self.offset_x)

    def update_volume(self, mouse_x: int) -> None:
        """
        updates the volume based on the mouse's x position
        """
        relative_position_of_the_knob = (mouse_x - self.scrollbar_x) / (self.scrollbar_width - self.knob_width)
        # calculate volume as a percentage of the bar's width
        self.volume = max(0, min(1, relative_position_of_the_knob))
        self._update_knob_position()

    def get_volume(self):
        return self.volume