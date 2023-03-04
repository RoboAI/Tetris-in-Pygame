import pygame
import math
import random
from Tetrimino import Tetrimino
from TetrimonoDot import TetriminoDot
from TetrimonoShape import TetriminoShape
from Globals import Globals
from Grid import Grid
from Wall import Wall
from MyFunctions import get_angle, get_distance, get_distance_from_pts

gb = Globals()

# get random shape
def get_next_random_shape():
    items = list(gb.GameShapes.items())
    item = random.choice(items)
    return item

# get random colour
def get_shape_colour(shape_name) -> str:
    colour = gb.GameShapeColours.get(shape_name)
    return colour


def setup_new_shape(game_shape):# game_shape is from Globals.GameShapes[i]
    new_shape = TetriminoShape()
    new_shape.desc = game_shape[0]
    new_shape.set_shape(game_shape[1][1])
    new_shape.rotation_index = game_shape[1][0]
    new_shape.set_pos(gb.grid_offset_x, gb.grid_offset_y, gb.grid_square_size)
    new_shape.add_to_pos(gb.grid_square_size * 7, gb.grid_square_size * -1)
    new_shape.set_colour(get_shape_colour(new_shape.desc))
    return new_shape


# copied above function as for some reason new_shape.set_pos isnt calling parent-classes function,
# which in turn is giving problems with initial position of the shape
def setup_next_shape(game_shape):# game_shape is from Globals.GameShape[i]
    new_shape = TetriminoShape()
    new_shape.desc = game_shape[0]
    new_shape.set_shape(game_shape[1][1])
    new_shape.rotation_index = game_shape[1][0]
    new_shape.set_pos(gb.infobox_next_shape_xy[0], gb.infobox_next_shape_xy[1], gb.grid_square_size)
    #new_shape.add_to_pos(gb.grid_square_size * 7, gb.grid_square_size * -1)
    new_shape.set_colour(get_shape_colour(new_shape.desc))
    return new_shape


# fix this: it works but get GameShapes should return {key: value} not just {value}
# then return should be: return setup_new_shape(found_item)
def get_new_shape_by_name(shape_name) -> TetriminoShape:
    found_item = gb.GameShapes.get(shape_name)
    return setup_new_shape([shape_name, found_item])


#setup grid
grid = Grid()

# time calculator for shapes movement interval
shapes_tick_interval = 750 # in milliseconds; move shape every xxx milliseconds

#used to calculate time between frames to control gameplay
time_passed = 0

#init pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([gb.screen_width, gb.screen_height])

# font setup
pygame.font.init()
next_shape_font = pygame.font.SysFont('Comic Sans MS', 30)
next_text_surface = next_shape_font.render('Next:', True, "navajowhite")
# score font
pygame.font.init()
score_font = pygame.font.SysFont('Comic Sans MS', 35)
score_text_surface = score_font.render('Score', True, "navajowhite")

# Get the Clock to limit frame-rate
clock = pygame.time.Clock()

# Run until the user asks to quit
running = True

# TODO: change grid_walls to dictionary
left_wall = [gb.grid_actual_rect[0], gb.grid_actual_rect[1]]
right_wall = [gb.grid_actual_rect[2], 0]
bottom_wall = [0, gb.grid_actual_rect[3]]
grid_walls = [["left-wall", left_wall], 
              ["right-wall", right_wall], 
              ["bottom-wall", bottom_wall]]


#-----------------
game_shapes = []
#game_shapes.remove(moving_dot)
#-----------------
single_layer = {}
all_layers = {}
for i in range(gb.grid_num_of_vt_squares - 1, -1, -1):#TODO: +10 for extra above
    single_layer = {i * gb.grid_square_size + gb.grid_offset_y: []}
    all_layers.update(single_layer)
    #a = all_layers[gb.grid_num_of_squares - 1 - i]
    #a.update({i * gb.grid_square_size: []})
#-----------------

# current shape
player_shape = get_next_random_shape()
player_shape = setup_new_shape(player_shape)
#-----------------

# next shape
player_next_shape = get_next_random_shape()
player_next_shape = setup_next_shape(player_next_shape)
#-----------------

# increment when collided with 'down'. When twice-> then block.moving == False
touched_down_count = 1

# draws a single TetriminoShape
def draw_shape(tetri_blocks: TetriminoShape):
    # loop trough all blocks drawing each
    for block in tetri_blocks.blocks:
        pygame.draw.circle(screen, block.colour, block.shape, gb.tetrimino_size, 100)
    

#TODO: this may be a duplicate of TetriminoShape.check_wall_collision()
def check_wall_collision(shape: Tetrimino, walls, str_wall):
    for block in shape.blocks:
        for single_wall in walls:
            if(single_wall[0] == str_wall):
                result = block.check_collision_with_wall(single_wall, gb.grid_square_size)
                if(result[0] == True):
                    return (result)
    return ([False, "none"])


# check collision with another shape
def check_if_shape_is_colliding(direction, shape: TetriminoShape):
    # check 'shape's collision with all other shapes
    for single_shape in game_shapes:
        # get the collision
        result = shape.check_collision_with_shape(direction, single_shape, gb.grid_block_distance)

        # if shape is colliding in that direction then don't do the move
        if(result[0] == True):
            return result
    
    return ([False, "none"])


def move_shape_right(shape: TetriminoShape, str_wall):
    # check for wall collisions
    result = check_wall_collision(shape, grid_walls, str_wall)
    if(result[0] == True):
        return False
    

# checks for collisions then moves a shape by one space
def move_shape_by_one(direction, shape: TetriminoShape, walls, wall_desc):
    
    #TODO: if 'direction' != 'str_wall', then no point checking walls
    # check for wall collisions
    result = check_wall_collision(shape, walls, wall_desc)
    if result[0] == True:
        if( (direction, result[1]) in Wall.wall_desc.items() ):
            return ([False, result[1]])


    # check for collisions with other shapes
    result = check_if_shape_is_colliding(direction, shape)
    if(result[0] == True):
        return ([False, result[1]])

    # no collision is detected so make the move according to 'direction'
    if(direction == "left"):
        shape.add_to_pos(-gb.grid_square_size, 0)
    elif(direction == "right"):
        shape.add_to_pos(gb.grid_square_size, 0)
    elif(direction == "up"):
        shape.add_to_pos(0, -gb.grid_square_size)
    elif(direction == "down"):
        shape.add_to_pos(0, gb.grid_square_size)
    
    # return 'success'
    return ([True, "none"])


# shift entire layers down once
def shift_layers_down_once(layers) -> None:
    # get the keys in sorted-reversed order to start from the highest-key
    # highest-key is incremented first, then lower etc
    # if we dont start from highest, then increasing key from lowest to the next layer
    # would overlap keys and so dictionary lookup will be invalid (duplicates)
    keys = list(layers.keys())
    keys.sort()
    keys.reverse()

    # loop to increment each key to the next value
    # save layer, pop it, modify key, then re-add
    for key in keys:
        blocks = layers[key]
        layers.pop(key)
        layers.update({key + gb.grid_square_size: blocks})


# create and re-add the popped layers
def add_missing_layers() -> None:
        keys = list(all_layers.keys())
        keys.sort()
        keys.reverse()
        for i in range(gb.grid_num_of_vt_squares - len(keys) - 1, -1, -1):#TODO: +10 for extra above
            single_layer = {i * gb.grid_square_size + gb.grid_offset_y: []}
            all_layers.update(single_layer)


# shape collided with bottom-wall
def shape_touched_down(current_shape: TetriminoShape):
    global player_shape
    global player_next_shape

    #pygame.display.set_caption("touch down")

    current_shape.moving = False
    
    game_shapes.append(player_shape)

    #------------------------
    # TODO: check if landed-shape has gone beyond upper-wall, then its game-over
    #------------------------

    #---------------------------------------------------
    # add current shape's blocks to the corresponding layers
    for block in player_shape.blocks:
        layer = all_layers.get(block.shape[1])
        layer.append(block)

    countx = 0
    layers_to_delete = []
    # loop through all layers
    for key in all_layers.keys():
        layer = all_layers.get(key)
        # if layer is full, then it means row is full so remove it
        if( len(layer) >= gb.grid_num_of_hz_squares ):
            # loop through all blocks in layer
            for block in layer:
                # loop through shapes checking which this block belongs to
                for shape in game_shapes:
                    # try to remove from parent
                    if( shape.remove_block(block) == True):
                        countx += 1
                        break
            layer.clear()
            layers_to_delete.append(key)
    
    if( (len(layers_to_delete)) > 0 ):

        for del_layer in layers_to_delete:
            all_layers.pop(del_layer)

        shift_layers_down_once(all_layers)
    
        add_missing_layers()

        for shape in game_shapes:
            shape.add_to_pos(0, gb.grid_square_size * len(layers_to_delete))
    #---------------------------------------------------
    
    #player_shape = get_new_shape_by_name("I")
    player_shape = get_new_shape_by_name(player_next_shape.desc)

    player_next_shape = get_next_random_shape()
    player_next_shape = setup_next_shape(player_next_shape)

    #pygame.display.set_caption(str(moving_dot.blocks[0]) + " " + moving_dot.blocks[0][1])


def check_and_remove_rows():
    pass

# move shape left one block
def move_shape_left_once(shape: TetriminoShape):
    return move_shape_by_one("left", shape, grid_walls, "left-wall")

# move shape right one block
def move_shape_right_once(shape: TetriminoShape):
    return move_shape_by_one("right", shape, grid_walls, "right-wall")

# move shape down one block
def move_shape_down_once(shape: TetriminoShape):
    result = move_shape_by_one("down", shape, grid_walls, "bottom-wall")
    if(result[0] == False):
      shape_touched_down(shape)

# move shape up one block
def move_shape_up_once(shape: TetriminoShape):
    return move_shape_by_one("up", shape, grid_walls, "bottom-wall")


# rotate shape clockwise
def rotate_shape_cw(shape: TetriminoShape, degrees):    
    for shape in game_shapes:
        if player_shape.check_rotation_collision(player_shape.blocks[player_shape.rotation_index].shape, degrees, shape, grid_walls, gb.grid_block_distance):
            break
    else:
        player_shape.rotate(player_shape.blocks[player_shape.rotation_index].shape, 90)


counter = 0

# main loop
while running:

    # set frame-rate and store time-elapsed since last frame
    time_passed += clock.tick(60)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # TODO: change grid_walls to dictionary
        elif event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_LEFT):
                move_shape_left_once(player_shape)
                    
            elif event.key == pygame.K_RIGHT:
                move_shape_right_once(player_shape)
                
            elif event.key == pygame.K_DOWN:
                move_shape_down_once(player_shape)

            elif event.key == pygame.K_UP:
                move_shape_up_once(player_shape)

            elif event.key == pygame.K_a:
                del player_shape.blocks[0]
            
            elif event.key == pygame.K_1:
                pass

            elif event.key == pygame.K_2:
                rotate_shape_cw(player_shape, 90)
            
            elif event.key == pygame.K_3:
                pass
            

    # Fill the background
    screen.fill(gb.grid_bk_colour)
    
    # draw left box
    pygame.draw.rect(screen, [60,60,60], gb.infobox_rect, gb.border_thickness)
    
    # draw grid-box
    pygame.draw.rect(screen, "black", gb.grid_rect, gb.border_thickness)

    # draw grid lines
    grid.draw_grid(pygame, screen)

    # draw 'next shape' text
    # screen.blit(next_text_surface, (gb.infobox_next_shape))

    # draw 'score' text
    screen.blit(score_text_surface, (gb.infobox_score_xy))

    # draw 'next shape'
    draw_shape(player_next_shape)

    #--------------------------------------------------------------
    if time_passed >= shapes_tick_interval :

        time_passed = 0

        if player_shape.moving == True:
            move_shape_down_once(player_shape)     
        
    #--------------------------------------------------------------

    # draw the moving one
    draw_shape(player_shape)

    # draw the rest of the shapes
    for game_shape in game_shapes:
        draw_shape(game_shape)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()