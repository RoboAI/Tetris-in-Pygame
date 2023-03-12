from Tetrimino import Tetrimino
from MyFunctions import get_angle, get_distance, get_distance_from_pts

#--------------------------
# TODO: remove these after finished
matrix = [[[j for j in range(5)] for i in range(4)] for x in range(2)]
print(matrix)

stocks = ['reliance', 'infosys', 'tcs']
prices = [2175, 1127, 2750]
mylist = [[2,2],[3,3],[4,4]]
mylist2 = [[1,1],[1,1],[-1,-1]]
mylist3 = [1,2,3,4,5]
mylist4 = [1]
a = zip(mylist3, mylist4)
print(set(a))
a = zip(stocks, prices)
print(set(a))
mylist3 = [1,2,3,4,5]
mylist4 = [1,4,5]
mylist1 = [[2,2],[3,3],[4,4],[5,5]]
mylist2 = [[3,3],[4,4]]
list1 = [i for i in mylist1 if i not in mylist2]
print(str(list1))
print(mylist4)
print(mylist1)
print(type(mylist4))
print(type(mylist1))
print("----------------------------------")
print("----------------------------------")
print("----------------------------------")
a = 5
b = a
b = 10
print(a)

#--------------------------

class Globals:
    def __init__(self):
        self.IBlock = [2, [[0,0],[1,0],[2,0],[3,0]]]
        self.TBlock = [3, [[0,0],[1,0],[2,0],[1,1]]]
        self.LBlock = [2, [[0,0],[0,1],[0,2],[1,2]]]
        self.JBlock = [2, [[1,0],[1,1],[1,2],[0,2]]]
        self.ZBlock = [2, [[0,0],[1,0],[1,1],[2,1]]]
        self.SBlock = [2, [[0,1],[1,1],[1,0],[2,0]]]
        self.SQBlock = [0, [[0,0],[1,0],[0,1],[1,1]]]

        self.GameShapeColours = {
                        "I": "orange",
                        "T": "red",
                        "L": "yellow",
                        "J": "brown",
                        "Z": "green",
                        "S": "purple",
                        "SQ": "light-blue"}

        self.GameShapes = {
                        "I": self.IBlock,
                        "T": self.TBlock,
                        "L": self.LBlock,
                        "J": self.JBlock,
                        "Z": self.ZBlock,
                        "S": self.SBlock,
                        "SQ": self.SQBlock}
    
    game_title = "Honest Game Studios"
    player_score_title = "Score"
    layers_score_title = "Layers"
    game_main_font = "Comic Sans MS"
    game_main_font_size = 30
    titles_font_colour = "navajowhite"
    scores_font_colour = "orange"
    game_over_font_colour = "firebrick"
    bounding_box_colour = "dimgray"
    top_pts_colour = "papayawhip"
    top_pts_size = 2
        
    game_over = False
    layers_cleared = 0
    player_score = 0
    player_level = 0 #not used
    row_cleared_points = 3
    multi_row_bonus = 5
    game_speed_increment = 100
    next_level_threshold = 2 # increase game speed after every 'x' layers cleared
    max_layers_cleared_speed_inc = 50 # > than this, then no more speed increase

    border_thickness = 1

    screen_width = 625
    screen_height = 500

    infobox_width = 200
    infobox_height = screen_height
    infobox_rect = [0,0,infobox_width, infobox_height]

    infobox_next_shape_xy: float = [infobox_width / 3, infobox_height / 5]

    infobox_text_offset = [infobox_width / 3 - 10, infobox_height - infobox_height / 2.5 - 20]
    infobox_score_title_xy: float = [infobox_text_offset[0], infobox_text_offset[1]]
    infobox_player_score_xy: float = [infobox_text_offset[0] + 30, infobox_text_offset[1] + 50]
    infobox_layer_title_xy: float = [infobox_text_offset[0] - 10, infobox_text_offset[1] + 110]
    infobox_layer_score_xy: float = [infobox_text_offset[0] + 30,  infobox_text_offset[1] + 160]


    grid_width = screen_width - infobox_width
    grid_height = screen_height
    grid_rect = [infobox_width, 0,
                grid_width, grid_height]
    
    grid_num_of_vt_squares: int = 20
    grid_num_of_hz_squares: int = grid_width / (grid_height / grid_num_of_vt_squares)

    grid_square_size = grid_height / grid_num_of_vt_squares
    grid_block_distance = get_distance(0, 0, grid_square_size, grid_square_size)
    grid_offset_x = grid_rect[0] + (grid_square_size / 2) + 1
    grid_offset_y = grid_rect[1] + (grid_square_size / 2) + 1
    grid_actual_rect = [grid_rect[0], grid_rect[1], grid_rect[0] + grid_width, grid_rect[1] + grid_height]
    grid_lines_colour = [35,35,35]
    grid_bk_colour = (25,25,25)

    grid_cel_rect = [0, 0, grid_square_size, grid_square_size]

    game_over_xy: float = [grid_width / 2 + infobox_width - 130,
                           grid_height / 2 - 20]

    # size of each Tetrimino block
    tetrimino_size = grid_square_size / 2 - 2

    # to stop typing it in
    grid_square_size_half = grid_square_size / 2



        # rc = pygame.Rect(block.shape[0], block.shape[1], gb.grid_square_size_half, gb.grid_square_size_half)
        # rc.move_ip(-gb.grid_square_size_half/2, -gb.grid_square_size_half/2)
        # rc.inflate_ip(gb.grid_square_size_half/2, gb.grid_square_size_half/2)
        # pygame.draw.rect(screen, block.colour, rc, 3)

        
        # self.GameShapeColours = {"I": "maroon",
        #                 "T": "tomato",
        #                 "L": "yellow",
        #                 "J": "blue",
        #                 "Z": "green",
        #                 "S": "lightseagreen",
        #                 "SQ": "silver"}

        

# sc_rect = pygame.Rect(0, 0, gb.screen_width, gb.screen_height)
# splash_anim.start_animation("Heaven", sc_rect)
#     if( splash_anim.update_animation() == True):
#             # Flip the display
#         pygame.display.flip()
#         continue