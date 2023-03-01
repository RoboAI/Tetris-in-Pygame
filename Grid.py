from Globals import Globals
from Tetrimino import Tetrimino
from TetrimonoShape import TetriminoShape
from MyFunctions import get_angle, get_distance, get_distance_from_pts

gb = Globals

class Grid:
    def __init__(self) -> None:
        pass

    def draw_grid(self, game, screen):
        pass

        start_x = gb.grid_rect[0]
        start_y = gb.grid_rect[1]
        end_x = start_x + gb.grid_width
        end_y = start_y + gb.grid_height
        grid_spacing = gb.grid_square_size

        # draw horizontal lines
        for y in range(end_y):
            game.draw.line(screen, 
                            gb.grid_lines_colour, 
                            (start_x, start_y + (y * grid_spacing)), 
                            (end_x, start_y + (y * grid_spacing)), 1)
                
        # draw vertical lines
        for x in range(end_x):
            game.draw.line(screen, 
                            gb.grid_lines_colour, 
                            (start_x + (x * grid_spacing), start_y), 
                            (start_x + (x * grid_spacing), end_y), 1)
            
abc = ([False, "none"])
print(type(abc))
abx = [False, "none"]