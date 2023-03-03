from Tetrimino import Tetrimino
from MyFunctions import get_angle, get_distance, get_distance_from_pts

class Globals:
    def __init__(self):
        self.IBlock = [2, [[0,0],[1,0],[2,0],[3,0]]]
        self.TBlock = [3, [[0,0],[1,0],[2,0],[1,1]]]
        self.LBlock = [2, [[0,0],[0,1],[0,2],[1,2]]]
        self.JBlock = [2, [[1,0],[1,1],[1,2],[0,2]]]
        self.ZBlock = [2, [[0,0],[1,0],[1,1],[2,1]]]
        self.SBlock = [2, [[0,1],[1,1],[1,0],[2,0]]]
        self.SQBlock = [0, [[0,0],[1,0],[0,1],[1,1]]]

        self.GameShapeColours = {"I": "orange",
                        "T": "red",
                        "L": "yellow",
                        "J": "blue",
                        "Z": "green",
                        "S": "lightseagreen",
                        "SQ": "brown"}

        self.GameShapes = {"I": self.IBlock,
                        "T": self.TBlock,
                        "L": self.LBlock,
                        "J": self.JBlock,
                        "Z": self.ZBlock,
                        "S": self.SBlock,
                        "SQ": self.SQBlock}

    border_thickness = 1

    screen_width = 625
    screen_height = 500

    infobox_width = 200
    infobox_height = screen_height
    infobox_rect = [0,0,infobox_width, infobox_height]

    infobox_next_shape_xy: float = [infobox_width / 3, infobox_height / 5]

    infobox_score_xy: float = [infobox_width / 3 - 10, infobox_height - infobox_height / 3]

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

