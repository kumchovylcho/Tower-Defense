import pygame as pg

import os
import configparser

from main_menu import constants


def load_image_from_assets(path: str, load_from="../assets", scale_to=None) -> pg.Surface:
    """
    The provided path must start from /assets folder.
    Example: map_images/blocks/grass.png or just image you are inside /assets folder already.

    scale_to: if provided it must be a tuple (to_width, to_height)
    """
    # to prevent path errors such as going too back in the path.
    path = path.lstrip("/")

    # this will point to inside main_menu folder
    current_dir = os.path.dirname(__file__)
    # will point to the assets folder from load_from arg
    assets_dir = os.path.abspath(os.path.join(current_dir, load_from))
    # the final target path
    target_image = os.path.join(assets_dir, path)
    loaded_img = pg.image.load(target_image)
    if scale_to:
        loaded_img = pg.transform.scale(loaded_img, scale_to)
    return loaded_img.convert_alpha()


def get_config_file_path() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # path to the config.cfg file, which is where main.py is located
    # going up one directory to access the config.ini file
    return os.path.join(os.path.dirname(base_dir), constants.CONFIG_FILE_NAME)


def get_volume_from_config(config: configparser.ConfigParser) -> float:
    try:
        volume_value = config.getfloat(constants.CONFIG_SOUND_SECTION,
                                       constants.CONFIG_SOUND_VOLUME_KEY,
                                       fallback=constants.CONFIG_DEFAULT_SOUND_VOLUME
                                       )
        if volume_value < 0 or volume_value > 1:
            volume_value = constants.CONFIG_DEFAULT_SOUND_VOLUME

        return volume_value
    except ValueError as e:
        # the value that the `CONFIG_SOUND_VOLUME_KEY` holds cant be cast to float, so we return the default value.
        print(e)
        return constants.CONFIG_DEFAULT_SOUND_VOLUME
