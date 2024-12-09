def is_valid_position(row: int, col: int, rows: int, cols: int) -> bool:
    return 0 <= row < rows and 0 <= col < cols


def create_matrix(rows: int, cols: int) -> list[list[int]]:
    matrix = []
    for row in range(rows):
        matrix.append(
            [0] * cols
        )
    return matrix


def create_matrix_with_monster_path(monster_path: tuple, rows: int, cols: int, path_width: int) -> list[list[int]]:
    """
    :param monster_path: ((row, col), (row, col), ...) where the first tuple is the starting point.
    :param rows: height of matrix
    :param cols: width of matrix
    :param path_width: the width of the path
    """
    start_pos = monster_path[0]
    remaining_monster_path = monster_path[1:]

    if not is_valid_position(start_pos[0], start_pos[1], rows, cols):
        raise ValueError(f"{start_pos} position is out of bounds.")

    directions = [
        (-1, -1),  # Up-Left
        (-1, 1),  # Up-Right
        (1, -1),  # Down-Left
        (1, 1),  # Down-Right
        (-1, 0),  # Up
        (1, 0),  # Down
        (0, -1),  # Left
        (0, 1)  # Right
    ]

    matrix = create_matrix(rows, cols)

    matrix[start_pos[0]][start_pos[1]] = 1
    for target in remaining_monster_path:
        if not is_valid_position(target[0], target[1], rows, cols):
            raise ValueError(f"{target} position is out of bounds.")

        # while target not reached
        while start_pos != target:
            row, col = start_pos

            for dx, dy in directions:
                new_x, new_y = row + dx, col + dy
                if not is_valid_position(new_x, new_y, rows, cols):
                    continue

                current_distance = abs(row - target[0]) + abs(col - target[1])
                new_distance = abs(new_x - target[0]) + abs(new_y - target[1])

                should_build_width = False
                # update position if we are getting closer to the target
                if new_distance < current_distance:
                    start_pos = (new_x, new_y)
                    should_build_width = True

                if should_build_width:
                    # 1. build width and break the loop
                    matrix[new_x][new_y] = 1
                    # break the loop, since new_distance < current_distance
                    break

    return matrix


drawed_path = create_matrix_with_monster_path(
    ((0, 0), (2, 2), (3, 4), (4, 4)),
    10,
    10,
    1
)
for row in drawed_path:
    print(row)