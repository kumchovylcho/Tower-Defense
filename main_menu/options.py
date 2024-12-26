import pygame as pg

from .utils import load_image_from_assets
from main_menu import constants


class Options:
    # TODO: Must crate a game package with constants inside so we can read the window size.
    def __init__(self):
        self.close_img = load_image_from_assets(constants.NORMAL_CLOSE_BUTTON_PATH)
        self.close_hover_img = load_image_from_assets(constants.HOVER_CLOSE_BUTTON_PATH)
        self.bg_frame = load_image_from_assets(constants.MENU_BACKGROUND_FRAME_IMAGE_PATH)

        self.static_surface = self._create_static_surface()

    def _create_static_surface(self) -> pg.Surface:
        pass