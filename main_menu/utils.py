import pygame as pg
import os


def load_image_from_assets(path: str, load_from="../assets") -> pg.Surface:
    """
    The provided path must start from /assets folder.
    Example: map_images/blocks/grass.png or just image you are inside /assets folder already.
    """
    # to prevent path errors such as going too back in the path.
    path = path.lstrip("/")

    # this will point to inside main_menu folder
    current_dir = os.path.dirname(__file__)
    # will point to the assets folder from load_from arg
    assets_dir = os.path.abspath(os.path.join(current_dir, load_from))
    # the final target path
    target_image = os.path.join(assets_dir, path)
    return pg.image.load(target_image).convert_alpha()