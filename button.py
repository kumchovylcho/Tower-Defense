import pygame

class Button:
    def __init__(self,
                 position: tuple,
                 normal_image_path: str,
                 hover_image_path: str,
                 callback=None):
        """
        Initializes the button with specific images for normal and hover states.

        :param position: Tuple (x, y) for the top-left corner of the button.
        :param normal_image_path: File path for the button's normal state image.
        :param hover_image_path: File path for the button's hover state image.
        :param callback: Function to call when the button is clicked.
        """
        self.x, self.y = position
        self.normal_image = pygame.image.load(normal_image_path).convert_alpha()
        self.hover_image = pygame.image.load(hover_image_path).convert_alpha()
        self.callback = callback
        self.is_hovered = False

        # Get the button's size from the image dimensions
        self.width, self.height = self.normal_image.get_size()

    def render(self, screen: pygame.Surface):
        """
        Draws the button on the screen.

        :param screen: The pygame Surface to draw on.
        """
        if self.is_hovered:
            screen.blit(self.hover_image, (self.x, self.y))
        else:
            screen.blit(self.normal_image, (self.x, self.y))

    def hover(self, mouse_position):
        """
        Updates hover state based on the mouse position.

        :param mouse_position: Tuple (mouse_x, mouse_y).
        """
        mouse_x, mouse_y = mouse_position
        self.is_hovered = (
            self.x <= mouse_x <= self.x + self.width and
            self.y <= mouse_y <= self.y + self.height
        )

    def click(self):
        """
        Executes the callback if the button is hovered and clicked.
        """
        if self.is_hovered and self.callback:
            self.callback()

    def handle_event(self, event: pygame.event.Event):
        """
        Handles mouse events for the button.

        :param event: A Pygame event (e.g., MOUSEMOTION or MOUSEBUTTONDOWN).
        """
        if event.type == pygame.MOUSEMOTION:
            self.hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
            self.click()



# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Button with Specific Images")

# Colors
WHITE = (255, 255, 255)


# Button Callback Function
def button_clicked():
    print("Button was clicked!")


# Create Button (Ensure the image paths are correct)
button = Button(
    position=(300, 250),  # Position of the button
    normal_image_path="assets/buttons/back_button_1.png",  # Normal state image file
    hover_image_path="assets/buttons/back_button_2.png",  # Hover state image file
    callback=button_clicked  # Function to call on click
)

# Game loop

# Quit Pygame
pygame.quit()
