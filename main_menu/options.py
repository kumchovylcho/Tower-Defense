import pygame as pg

from .utils import load_image_from_assets
from main_menu import constants as menu_constants
from game import constants as game_constants
from ui.horizontal_scrollbar import HorizontalVolumeScrollbar
from ui.button import Button


class Options:

    def __init__(self, screen: pg.Surface):
        self.bg_frame = load_image_from_assets(
            menu_constants.MENU_BACKGROUND_FRAME_IMAGE_PATH,
            scale_to=menu_constants.FRAME_DIMENSIONS
        )

        window_width, window_height = game_constants.DIMENSIONS
        self.frame_x = window_width // 2 - self.bg_frame.get_width() // 2
        self.frame_y = window_height // 2 - self.bg_frame.get_height() // 2

        self.volume_scrollbar = HorizontalVolumeScrollbar(
            screen,
            (self.frame_x + menu_constants.SCROLLBAR_RELATIVE_TO_FRAME_X,
             self.frame_y + menu_constants.SCROLLBAR_RELATIVE_TO_FRAME_Y,
             menu_constants.SCROLLBAR_WIDTH,
             menu_constants.SCROLLBAR_HEIGHT
             ),
            menu_constants.SCROLLBAR_COLOR,
            (menu_constants.KNOB_WIDTH, menu_constants.KNOB_HEIGHT),
            menu_constants.KNOB_COLOR,
            scrollbar_border_radii=menu_constants.SCROLLBAR_BORDER_RADII,
            knob_border_radii=menu_constants.KNOB_BORDER_RADII,
        )

        self.close_btn = Button(
            (self.frame_x + menu_constants.CLOSE_BTN_RELATIVE_TO_FRAME_POSITION[0],
             self.frame_y + menu_constants.CLOSE_BTN_RELATIVE_TO_FRAME_POSITION[1]
             ),
            load_image_from_assets(
                menu_constants.NORMAL_CLOSE_BUTTON_PATH,
                scale_to=menu_constants.CLOSE_BTN_SIZE
            ),
            load_image_from_assets(
                menu_constants.HOVER_CLOSE_BUTTON_PATH,
                scale_to=menu_constants.CLOSE_BTN_SIZE
            ),
            on_hover_cursor=pg.SYSTEM_CURSOR_HAND
        )
        self.ok_btn = Button(
            (self.frame_x + menu_constants.OK_BTN_RELATIVE_TO_FRAME_POSITION[0],
             self.frame_y + menu_constants.OK_BTN_RELATIVE_TO_FRAME_POSITION[1]
             ),
            load_image_from_assets(
                menu_constants.NORMAL_OK_BUTTON_PATH,
                scale_to=menu_constants.OK_BTN_SIZE
            ),
            load_image_from_assets(
                menu_constants.HOVER_OK_BUTTON_PATH,
                scale_to=menu_constants.OK_BTN_SIZE
            ),
            on_hover_cursor=pg.SYSTEM_CURSOR_HAND
        )

        self.buttons = [self.close_btn, self.ok_btn]

        self.volume_font = pg.font.Font(None, menu_constants.VOLUME_TEXT_SIZE)
        self.volume_surface = self._create_volume_surface()
        self.volume_text_x = self._recenter_volume_surface()
        self.volume_text_y = self.frame_y + menu_constants.VOLUME_TEXT_POSITION_Y

    def _render_buttons(self, surface: pg.Surface) -> None:
        for button in self.buttons:
            button.render(surface)

    def _create_volume_surface(self) -> pg.Surface:
        return self.volume_font.render(f"Volume: {int(self.volume_scrollbar.get_volume() * 100)}%",
                                       True,
                                       menu_constants.VOLUME_TEXT_COLOR
                                       ).convert_alpha()

    def _recenter_volume_surface(self) -> int:
        return self.frame_x + (menu_constants.FRAME_DIMENSIONS[0] - self.volume_surface.get_width()) // 2

    def render(self, screen: pg.Surface) -> None:
        screen.blit(self.bg_frame, (self.frame_x, self.frame_y))
        self.volume_scrollbar.draw()

        if self.volume_scrollbar.has_volume_changed():
            self.volume_surface = self._create_volume_surface()
            self.volume_text_x = self._recenter_volume_surface()

        screen.blit(self.volume_surface, (self.volume_text_x, self.volume_text_y))
        self._render_buttons(screen)
