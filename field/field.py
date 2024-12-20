import pygame as pg
from random import choice

from field.tile import Tile


class Field:
    OBSTACLE_POSITIONS = "obstacle_positions"
    OBSTACLE_IMAGES = "obstacle_images"
    PATH_TILE = "path_tile"
    PATH_WIDTH = "path_width"
    BUILDABLE_TILE = "buildable_tile"
    HOVER_COLOR_ON_TILES = "hover_color_on_tiles"

    def __init__(self, monster_path: tuple, field_dimensions: tuple, screen_dimensions: tuple, config: dict):
        """
        :param monster_path: ((row, col), (row, col), ...) where the first tuple is the starting point.
        :param field_dimensions: (rows, cols, tile_size)
        :param screen_dimensions: (screen_width, screen_height) - needed for centering the field
        :param config: a dictionary with keys where:
            "obstacle_positions": ((row, col), (row, col)...) tuple of tuples containing positions for the obstacles
            "obstacle_images": [], list with loaded and scaled images of obstacles
            "path_tile": loaded and scaled image that will be used for the path
            "path_width": integer representing how many tiles should the width of the path be
            "buildable_tile": loaded and scaled image that will be used for regular/buildable blocks
            "hover_color_on_tiles": (255, 255, 0, 128) tuple (r, g, b, a)
        """
        self.config = config
        self.monster_path = monster_path
        self.field: [Tile] = []
        self.rows, self.cols, self.tile_size = field_dimensions
        self.field_width = self.cols * self.tile_size
        self.field_height = self.rows * self.tile_size
        self.x_offset, self.y_offset = self.get_centering_offset(screen_dimensions)

        self.static_surface = None

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        if not isinstance(value, dict):
            raise ValueError("Must provide a dictionary.")

        if not value.get(self.BUILDABLE_TILE):
            raise ValueError("Please provide regular buildable tile image.")

        if not value.get(self.HOVER_COLOR_ON_TILES):
            raise ValueError("Please provide hover color on the tiles.")

        if not isinstance(value.get(self.OBSTACLE_IMAGES), (list, tuple)):
            raise ValueError("Please provide a list or tuple with obstacles. Can be empty.")

        if not value.get(self.PATH_TILE):
            raise ValueError("Please provide image for the path tile.")

        path_width = value.get(self.PATH_WIDTH)
        if not path_width or not isinstance(path_width, int) or path_width <= 0:
            raise ValueError("Please provide path width with correct integer value. It should be more than 0.")

        obstacle_positions = value.get(self.OBSTACLE_POSITIONS)
        # if the outer expecting tuple is not a tuple
        if (not isinstance(obstacle_positions, tuple) or
                # if any of the inner tuples are not tuples
                any(not isinstance(tup, tuple) for tup in obstacle_positions)
        ):
            raise ValueError("Please provide correct tuple format. ((row, col), (row, col)). or empty tuple.")

        self.__config = value

    @staticmethod
    def all_directions() -> list[tuple[int, int]]:
        return [
            (-1, -1),  # Up-Left
            (-1, 1),  # Up-Right
            (1, -1),  # Down-Left
            (1, 1),  # Down-Right
            (-1, 0),  # Up
            (1, 0),  # Down
            (0, -1),  # Left
            (0, 1)  # Right
        ]

    def get_centering_offset(self, screen_dimensions: tuple) -> tuple:
        screen_width, screen_height = screen_dimensions
        x_offset = (screen_width - self.field_width) // 2
        y_offset = (screen_height - self.field_height) // 2
        return x_offset, y_offset

    def create_static_surface(self) -> None:
        if not self.field:
            raise ValueError("Field must be created first.")

        self.static_surface = pg.Surface((self.field_width + self.x_offset,
                                     self.field_height + self.y_offset),
                                    pg.SRCALPHA)
        self.static_surface.fill((0, 0, 0, 0))
        for row in self.field:
            for tile in row:
                self.static_surface.blit(tile.image, tile.image_rect.topleft)

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def create_matrix(self) -> None:
        normal_tile_img = self.config.get(self.BUILDABLE_TILE)
        hover_color = self.config.get(self.HOVER_COLOR_ON_TILES)

        for row in range(self.rows):
            current_row = []
            for col in range(self.cols):
                tile = Tile(
                    image=normal_tile_img,
                    position=(
                        col * self.tile_size + self.x_offset,
                        row * self.tile_size + self.y_offset
                    ),
                    hover_color=hover_color
                )

                current_row.append(tile)

            self.field.append(current_row)

    def place_obstacles(self) -> None:
        obstacle_positions = self.config.get(self.OBSTACLE_POSITIONS)
        obstacle_images = self.config.get(self.OBSTACLE_IMAGES)
        # place obstacles if any
        if obstacle_images and obstacle_positions:
            for row, col in obstacle_positions:
                if not self.is_valid_position(row, col):
                    raise ValueError(f"({row}, {col}) obstacle is out of bounds.")

                # check if we try to place the obstacle on the monster path
                tile = self.field[row][col]
                if tile.is_path_or_obstacle:
                    raise ValueError(f"({row}, {col}) position is trying to be placed on the monster path.")

                # place the obstacle
                tile.image = choice(obstacle_images)
                tile.is_path_or_obstacle = True

    def spread_path_width(self, from_position: tuple[int, int], width: int, path_img: pg.Surface) -> None:
        x, y = from_position
        # this is done like that, so it works for even numbers.
        # for example if we don't subtract by 1 and the width is 2, then
        # the result will be 4 tiles of width instead of 2
        radius = (width - 1) // 2
        # needed so it handles the even integers of width properly
        compare_radius = radius + (1 if width % 2 == 0 else 0)
        # +2 to ensure the path is correctly spread out in both horizontal and vertical directions
        for dx in range(-radius, radius + 2):
            for dy in range(-radius, radius + 2):
                # skip if this is outside the path of the width provided
                if not abs(dx) + abs(dy) <= compare_radius:
                    continue

                new_x, new_y = x + dx, y + dy
                if not self.is_valid_position(new_x, new_y):
                    continue

                tile = self.field[new_x][new_y]
                if tile.is_path_or_obstacle:
                    continue

                tile.image = path_img
                tile.is_path_or_obstacle = True


    def create_field(self) -> None:
        start_pos = self.monster_path[0]
        remaining_monster_path = self.monster_path[1:]

        if not self.is_valid_position(start_pos[0], start_pos[1]):
            raise ValueError(f"{start_pos} position is out of bounds.")

        path_img = self.config.get(self.PATH_TILE)
        path_width = self.config.get(self.PATH_WIDTH)
        directions = self.all_directions()

        self.create_matrix()
        self.spread_path_width(start_pos, path_width, path_img)
        for target in remaining_monster_path:
            if not self.is_valid_position(target[0], target[1]):
                raise ValueError(f"{target} position is out of bounds.")

            # while target not reached
            while start_pos != target:
                row, col = start_pos

                for dx, dy in directions:
                    new_x, new_y = row + dx, col + dy
                    if not self.is_valid_position(new_x, new_y):
                        continue

                    current_distance = abs(row - target[0]) + abs(col - target[1])
                    new_distance = abs(new_x - target[0]) + abs(new_y - target[1])

                    # update position if we are getting closer to the target
                    # break the loop, since new_distance < current_distance
                    if new_distance < current_distance:
                        start_pos = (new_x, new_y)
                        self.spread_path_width((new_x, new_y), path_width, path_img)
                        break

        self.place_obstacles()
        # create the static surface after field generation
        self.create_static_surface()

    def render_tiles(self, surface_to_draw_on: pg.Surface) -> None:
        surface_to_draw_on.blit(self.static_surface, (0, 0))
        for row in self.field:
            for tile in row:
                tile.render_block(surface_to_draw_on)
