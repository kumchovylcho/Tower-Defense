import pygame as pg
import configparser

from utils import draw_gradient
import constants
from camera_movement import CameraMovement


# load user settings
config = configparser.ConfigParser()
config.read("CONFIG.cfg")


# Initialize Pygame
pg.init()

# Clock for capping FPS
clock = pg.time.Clock()


# camera settings
camera = CameraMovement(camera_x=constants.INITIAL_CAMERA_X,
                        camera_y=constants.INITIAL_CAMERA_Y,
                        zoom_level=constants.ZOOM_LEVEL,
                        min_zoom=constants.MIN_ZOOM,
                        max_zoom=constants.MAX_ZOOM,
                        zoom_speed=constants.ZOOM_SPEED,
                        zoom_step_speed=constants.ZOOM_STEP_SPEED,
                        drag_friction=constants.DRAG_FRICTION_WHEN_DRAG_ENDS,
                        drag_momentum_threshold=constants.DRAG_MOMENTUM_THRESHOLD
                        )

# load tile
scaled_image = pg.transform.scale(
    pg.image.load("assets/map_images/blocks/grass_2.png"),
    (constants.TILE_SIZE, constants.TILE_SIZE)
)

# Screen settings
WIDTH, HEIGHT = int(config["Display"]["WIDTH"]), int(config["Display"]["HEIGHT"])
IS_GRADIENT_BACKGROUND = bool(int(config["Display"]["GRADIENT"]))
REGULAR_BACKGROUND_COLOR = [int(color) for color in config["Display"]["BACKGROUND_COLOR"].split(", ")]
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tower-Defense")
if IS_GRADIENT_BACKGROUND:
    GRADIENT_START = [int(color) for color in config["Display"]["GRADIENT_START"].split(", ")]
    GRADIENT_END = [int(color) for color in config["Display"]["GRADIENT_END"].split(", ")]


# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEWHEEL:
            camera.adjust_zoom_level(event.y)
        elif event.type == pg.MOUSEBUTTONDOWN:
            camera.activate_dragging_camera(event.button == 1, False)
        elif event.type == pg.MOUSEBUTTONUP:
            camera.activate_dragging_camera(False, event.button == 1)

    camera.move_camera()

    # fill background with some color if the user wants so
    if not IS_GRADIENT_BACKGROUND:
        screen.fill(REGULAR_BACKGROUND_COLOR)
    else:
        draw_gradient.draw_gradient(
            screen,
            GRADIENT_START,
            GRADIENT_END,
            config["Display"]["GRADIENT_DIRECTION"].lower()
        )

    # Update display
    pg.display.flip()
    clock.tick(constants.FPS)

pg.quit()