import pygame as pg


def draw_gradient(surface: pg.Surface, start_color: list[int], end_color: list[int], direction="vertical") -> None:
    """
    Draws a gradient on the given surface.

    Args:
        surface: Pygame surface to draw on.
        start_color: Starting color of the gradient (RGB tuple).
        end_color: Ending color of the gradient (RGB tuple).
        direction: "vertical" or "horizontal" for gradient direction.
    """
    width, height = surface.get_size()
    if direction == "vertical":
        for y in range(height):
            color = [
                start_color[i] + (end_color[i] - start_color[i]) * y // height
                for i in range(3)
            ]
            pg.draw.line(surface, color, (0, y), (width, y))
    elif direction == "horizontal":
        for x in range(width):
            color = [
                start_color[i] + (end_color[i] - start_color[i]) * x // width
                for i in range(3)
            ]
            pg.draw.line(surface, color, (x, 0), (x, height))