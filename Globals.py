from Tetrimino import Tetrimino
from MyFunctions import get_angle, get_distance, get_distance_from_pts

class Globals:
    border_thickness = 1

    screen_width = 625
    screen_height = 500

    infobox_width = 200
    infobox_height = screen_height
    infobox_rect = [0,0,infobox_width, infobox_height]

    grid_num_of_squares = 20
    grid_width = screen_width - infobox_width
    grid_height = screen_height
    grid_rect = [infobox_width, 0,
                grid_width, grid_height]

    grid_square_size = grid_height / grid_num_of_squares
    grid_block_distance = get_distance(0, 0, grid_square_size, grid_square_size)
    grid_offset_x = grid_rect[0] + (grid_square_size / 2) + 1
    grid_offset_y = grid_rect[1] + (grid_square_size / 2) + 1
    grid_actual_rect = [grid_rect[0], grid_rect[1], grid_rect[0] + grid_width, grid_rect[1] + grid_height]
    grid_lines_colour = [35,35,35]
    grid_bk_colour = (25,25,25)

    grid_cel_rect = [0, 0, grid_square_size, grid_square_size]

    # size of each Tetrimino block
    tetrimino_size = grid_square_size / 2 - 2

    IBlock = [[0,0],[1,0],[2,0],[3,0],[4,0]]
    TBlock = [[0,0],[1,0],[2,0],[1,1],[1,2]]
    LBlock = [[0,0],[0,1],[0,2],[0,3],[1,3]]
    JBlock = [[1,0],[1,1],[1,2],[1,3],[0,3]]
    ZBlock = [[0,0],[1,0],[1,1],[2,1]]
    SBlock = [[0,1],[1,1],[1,0],[2,0]]
    SQBlock = [[0,0],[1,0],[0,1],[1,1]]