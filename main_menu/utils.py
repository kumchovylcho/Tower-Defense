import pygame as pg
import os


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