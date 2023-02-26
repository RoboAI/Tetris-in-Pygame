import pygame
import math
from Tetrimino import Tetrimino
from TetrimonoDot import TetriminoDot
from TetrimonoShape import TetriminoShape
from MyFunctions import get_angle, get_distance, get_distance_from_pts

def draw_grid(box_top):
    start_x = grid_rect[0]
    start_y = grid_rect[1]
    end_x = start_x + grid_width
    end_y = start_y + grid_height
    grid_spacing = grid_square_size

    for y in range(end_y):
        pygame.draw.line(screen, 
                         "blue", 
                         (start_x, start_y + (y * grid_spacing)), 
                         (end_x, start_y + (y * grid_spacing)), 1)
        if(y == 3):
            pygame.draw.line(screen, 
                         "pink", 
                         (start_x, start_y + (y * grid_spacing)), 
                         (end_x, start_y + (y * grid_spacing)), 1)
            

    for x in range(end_x):
        pygame.draw.line(screen, 
                         "blue", 
                         (start_x + (x * grid_spacing), start_y), 
                         (start_x + (x * grid_spacing), end_y), 1)
        
class SingleSquare:
    def __init__(self):
        self.x_pos: float = 0
        self.y_pos: float = 0
        self.rect = [0,0,0,0]

    def move_me(self, x:float, y:float):
        self.rect[0] += x
        self.rect[1] += y

IBlock = [[0,0],[1,0],[2,0],[3,0],[4,0]]
TBlock = [[0,0],[1,0],[2,0],[1,1],[1,2],[1,3]]
LBlock = [[0,0],[0,1],[0,2],[0,3],[1,3]]
ZBlock = [[0,0],[1,0],[1,1],[2,1]]
SQBlock = [[0,0],[1,0],[0,1],[1,1]]

pygame.init()

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

# time calculator for shapes movement interval
shapes_tick_interval = 750 # in milliseconds; move shape every xxx milliseconds

# Set up the drawing window
screen = pygame.display.set_mode([screen_width, screen_height])

counter = 0

#used to calculate time between frames to control gameplay
time_passed = 0

# Get the Clock to limit frame-rate
clock = pygame.time.Clock()

# Run until the user asks to quit
running = True

single_box = SingleSquare()
single_box.rect = [grid_rect[0], 0, grid_square_size, grid_square_size]
#-----------------
single_dot = TetriminoDot(0, 0)
single_dot.set_pos(grid_offset_x, grid_offset_y)
single_dot.add_to_pos(grid_square_size * 5, grid_square_size * 5)
#------------------
moving_dot = TetriminoDot(0,0)
moving_dot.set_pos(grid_offset_x, grid_offset_y)
moving_dot.add_to_pos(grid_square_size, grid_square_size)
moving_dot.moving = False
#-------------.txt----
I_block = TetriminoShape()
I_block.set_shape(IBlock.copy())
I_block.set_pos(grid_offset_x, grid_offset_y, grid_square_size)
I_block.add_to_pos(grid_square_size * 6, grid_square_size * 7)
I_block.set_colour("red")
#-----------------
T_block = TetriminoShape()
T_block.set_shape(TBlock.copy())
T_block.set_pos(grid_offset_x, grid_offset_y, grid_square_size)
T_block.add_to_pos(grid_square_size * 4, grid_square_size)
T_block.set_colour("dark blue")
#-----------------
L_block = TetriminoShape()
L_block.set_shape(LBlock.copy())
L_block.set_pos(grid_offset_x, grid_offset_y, grid_square_size)
L_block.add_to_pos(grid_square_size * 2, grid_square_size * 7)
L_block.set_colour("dark green")
#-----------------
Z_block = TetriminoShape()
Z_block.set_shape(ZBlock.copy())
Z_block.set_pos(grid_offset_x, grid_offset_y, grid_square_size)
Z_block.add_to_pos(grid_square_size * 6, grid_square_size * 12)
Z_block.set_colour("dark orange")
#-----------------
SQ_block = TetriminoShape()
SQ_block.set_shape(SQBlock.copy())
SQ_block.set_pos(grid_offset_x, grid_offset_y, grid_square_size)
SQ_block.add_to_pos(grid_square_size * 10, grid_square_size * 16)
SQ_block.set_colour("brown")
#-----------------
moving_dot = T_block
game_shapes = [I_block, L_block, Z_block, SQ_block]



def draw_shape(tetri_blocks: TetriminoShape):
    for block in tetri_blocks.blocks:
        pygame.draw.circle(screen, block.colour, block.shape, 10, 10)
    

def move_shape_by_one(direction, shape: TetriminoShape):
    for single_shape in game_shapes:
        result = moving_dot.check_collision_with_shape(direction, single_shape, grid_block_distance)
        if(result[0] == True):
            return

    if(direction == "left"):
        shape.add_to_pos(-grid_square_size, 0)
    elif(direction == "right"):
        shape.add_to_pos(grid_square_size, 0)
    elif(direction == "up"):
        shape.add_to_pos(0, -grid_square_size)
    elif(direction == "down"):
        shape.add_to_pos(0, grid_square_size)


counter2 = 0
while running:
    # set frame-rate
    time_passed += clock.tick(60)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_LEFT):
                move_shape_by_one("left", moving_dot)
                    
            elif event.key == pygame.K_RIGHT:
                move_shape_by_one("right", moving_dot)

            elif event.key == pygame.K_UP:
                move_shape_by_one("up", moving_dot)

            elif event.key == pygame.K_DOWN:
                move_shape_by_one("down", moving_dot)

            elif event.key == pygame.K_a:
                del moving_dot.blocks[0]

            #get_angle(moving_dot.shape, single_dot.shape)
            #get_distance_from_pts(moving_dot.shape, single_dot.shape)
            #get_distance(0,0,grid_square_size, grid_square_size)

    # Fill the background with white
    screen.fill((255, 255, 255))
    
    pygame.draw.rect(screen, "green", infobox_rect, border_thickness)
    pygame.draw.rect(screen, "red", grid_rect, border_thickness)

    draw_grid(single_box.y_pos)

    #--------------------------------------------------------------
    if time_passed >= shapes_tick_interval :
        #pygame.display.set_caption(str(time_passed))
        time_passed = 0

        #if moving_dot.moving == True:
            # do a dummy move to check for collision
            #moving_dot.add_to_pos(grid_square_size, grid_square_size)

            # if colliding..
            # if moving_dot.check_collision(single_dot, single_dot):
                #stop object
                #moving_dot.moving = False
                # move the object back to its previous point
                #moving_dot.add_to_pos(-grid_square_size, -grid_square_size)
                #pygame.display.set_caption("Collided!! ")

        move_shape_by_one("down", moving_dot)        
        
    #--------------------------------------------------------------

    draw_shape(moving_dot)
    for game_shape in game_shapes:
        draw_shape(game_shape)

    # Flip the display
    pygame.display.flip()

    counter += 1

# Done! Time to quit.
pygame.quit()