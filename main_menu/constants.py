# FRAME DIMENSIONS
FRAME_DIMENSIONS = (400, 500)
# END FRAME SETTINGS



# MAIN MENU RELATIVE IMAGE PATHS THAT WILL BE LOADED FROM MAIN_MENU FOLDER
MENU_BACKGROUND_FRAME_IMAGE_PATH = "menu_images/initial_menu/background_menu/menu_background.png"
# END MENU RELATIVE IMAGE PATHS SETTINGS



# OPTIONS RELATIVE IMAGE PATHS THAT WILL BE LOADED FROM MAIN_MENU FOLDER
NORMAL_CLOSE_BUTTON_PATH = "menu_images/options_menu/buttons/close_normal.png"
HOVER_CLOSE_BUTTON_PATH = "menu_images/options_menu/buttons/close_hover.png"
NORMAL_OK_BUTTON_PATH = "menu_images/options_menu/buttons/ok_btn_green.png"
HOVER_OK_BUTTON_PATH = "menu_images/options_menu/buttons/ok_btn_honey.png"

# OPTIONS MENU BUTTON SIZES
CLOSE_BTN_SIZE = (40, 36)
CLOSE_BTN_RELATIVE_TO_FRAME_POSITION = (300, 10)
# if in the future you want a bigger or smaller button the aspect ratio is 198 / 70 = 2.83
# to make it smaller or bigger you must keep the 2.83 ratio
OK_BTN_SIZE = (198, 70)
OK_BTN_RELATIVE_TO_FRAME_POSITION = (FRAME_DIMENSIONS[0] // 2 - OK_BTN_SIZE[0] // 2, 350)

# VOLUME SCROLLBAR SETTINGS
SCROLLBAR_WIDTH = 300
SCROLLBAR_HEIGHT = 15
SCROLLBAR_RELATIVE_TO_FRAME_X = FRAME_DIMENSIONS[0] // 2 - SCROLLBAR_WIDTH // 2
SCROLLBAR_RELATIVE_TO_FRAME_Y = 100
SCROLLBAR_COLOR = (128, 128, 128)
SCROLLBAR_BORDER_RADII = {"border_radius": 12}
VOLUME_TEXT_SIZE = 36
VOLUME_TEXT_COLOR = (0, 0, 0)
VOLUME_TEXT_POSITION_Y = SCROLLBAR_RELATIVE_TO_FRAME_Y - 40

# KNOB SETTINGS
KNOB_WIDTH = 20
KNOB_HEIGHT = 20
KNOB_COLOR = (0, 200, 0)
KNOB_BORDER_RADII = {"border_radius": KNOB_WIDTH // 2}
# END OPTION SETTINGS


# CONFIG.CFG FILE NAME
CONFIG_FILE_NAME = "CONFIG.cfg"
CONFIG_SOUND_SECTION = "Sound"
CONFIG_SOUND_VOLUME_KEY = "VOLUME"
CONFIG_DEFAULT_SOUND_VOLUME = 0.5
# END CONFIG SETTINGS