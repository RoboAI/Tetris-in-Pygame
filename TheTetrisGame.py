import pygame
import math
import random
from Tetrimino import Tetrimino
from TetrimonoDot import TetriminoDot
from TetrimonoShape import TetriminoShape
from Globals import Globals
from Grid import Grid
from Wall import Wall
from SplashScreen import SplashScreen
from ShapeImages import ShapeImages
from ScoreBoard import ScoreBoard
from SoundManager import SoundManager
from AutoDownMoveInterval import AutoDownMoveInterval
from MyFunctions import get_angle, get_distance, get_distance_from_pts, get_points_on_top


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
    new_shape.add_to_pos(gb.grid_square_size * 7, gb.grid_square_size * -2)
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


# start main theme
sound_manager = SoundManager()
sound_manager.play_main_theme()
#---------------------

#setup grid
grid = Grid()
#---------------------

# these control the speed of the moving shape
auto_move_interval = AutoDownMoveInterval(750, 50) # original value/normal speed
auto_move_interval_fast = AutoDownMoveInterval(50, 50) # temporarily used to speed-up/slow-down the game
auto_move_interval_actual = auto_move_interval # actual value used to apply to the game. switches between the two
#---------------------

#used to calculate time between frames to control gameplay
time_passed = 0
#---------------------

#init pygame
pygame.init()
#---------------------

# Set up the drawing window
screen = pygame.display.set_mode([gb.screen_width, gb.screen_height])
#---------------------

# window title
pygame.display.set_caption(gb.game_title)
#---------------------

# font setup
pygame.font.init()
#---------------------

# score board
score_board = ScoreBoard(pygame)
score_board.init_fonts(gb.titles_font_colour, gb.scores_font_colour, gb.layers_score_title, gb.player_score_title)
#---------------------

# game over font
game_over_font = pygame.font.SysFont(gb.game_main_font, 50)
game_over_surface = game_over_font.render('Game Over', True, gb.game_over_font_colour)
#---------------------

# Get the Clock to limit frame-rate
clock = pygame.time.Clock()
#---------------------

# Run until the user asks to quit
running = True
#---------------------

# menu loop
in_menu = True
#---------------------

# TODO: change grid_walls to dictionary
left_wall = [gb.grid_actual_rect[0], gb.grid_actual_rect[1]]
right_wall = [gb.grid_actual_rect[2], 0]
bottom_wall = [0, gb.grid_actual_rect[3]]
grid_walls = [["left-wall", left_wall], 
              ["right-wall", right_wall], 
              ["bottom-wall", bottom_wall]]
#---------------------


#---------------------
game_shapes = []
#---------------------

# grid layers. stores the blocks in layers.
all_layers = {}
for i in range(gb.grid_num_of_vt_squares - 1, -1, -1):#TODO: +10 for extra above
    all_layers.update({i * gb.grid_square_size + gb.grid_offset_y: []})
#---------------------

# current shape
player_shape = get_next_random_shape()
player_shape = setup_new_shape(player_shape)
#---------------------
# player_shape = get_new_shape_by_name("S")
# player_shape.blocks[0].colour = "blue"
# player_shape.blocks[1].colour = "green"
# player_shape.blocks[2].colour = "orange"
# player_shape.blocks[3].colour = "yellow"
#---------------------

# next shape
player_next_shape = get_next_random_shape()
player_next_shape = setup_next_shape(player_next_shape)
#---------------------

# shape markers
bounding_box = None
top_pts = None # markers for shape's top-coords
draw_bounding_box = False
#---------------------

# increment when collided with 'down'. When twice-> then block.moving == False
touched_down_count = 1
#---------------------

#---------------------
images = ShapeImages(pygame)
rc = pygame.Rect(0, 0, 27, 27)
images.add_image("brown", "images/brown-low.png", rc)
images.add_image("green", "images/green-low.png", rc)
images.add_image("yellow", "images/yellow-low.png", rc)
images.add_image("orange", "images/orange-low.png", rc)
images.add_image("purple", "images/purple-low.png", rc)
images.add_image("light-blue", "images/light-blue-low.png", rc)
images.add_image("red", "images/red-low.png", rc)
#---------------------

splash_anim = SplashScreen(pygame, screen)
#---------------------

temp_rows_cleared_counter = 0
#---------------------

#---------------------------------------------------------
# draws a single TetriminoShape
def draw_shape(tetri_blocks: TetriminoShape):
    # loop trough all blocks drawing each
    for block in tetri_blocks.blocks:
        dict_img = (images.sprites[block.colour])
        rc = dict_img[0].move(block.shape[0]-gb.grid_square_size_half, block.shape[1]-gb.grid_square_size_half)
        screen.blit(dict_img[1], rc)


# TODO: move displaying-GameOver stuff here
def display_gameover():
    pass
#---------------------------------------------------------


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


# checks for collisions then moves a shape by one space
def move_shape_by_one(direction, shape: TetriminoShape, walls, wall_desc):
    
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

    update_bounding_box(shape)
    update_top_points(shape)
    
    # return 'success'
    return ([True, "none"])


def remove_layers(dict_layers, layers) -> None:
    for key in layers:
        # get the TetriminoDots
        blocks = dict_layers[key]

        # remove the TetriminoDots from their parents for deletion
        remove_layer_blocks_from_parents(blocks)

        # remove references. TODO: check if needed
        dict_layers[key].clear()

        # remove from all_layers
        dict_layers.pop(key)


def remove_layer_blocks_from_parents(layer: list):
    # this nested loop removes all the blocks in the layer from their parents.
    # loop through all blocks in layer
    for block in layer:
        # loop through shapes checking which this block belongs to
        for shape in game_shapes:
            # try to remove from parent
            if( shape.remove_block(block) == True):
                break


def get_completed_rows() -> list:
    # get the rows that contains more than 'gb.grid_num_of_hz_squares' blocks 
    layers_to_delete = [i for i in all_layers.keys() 
                         if len(all_layers.get(i)) >= gb.grid_num_of_hz_squares ]
    
    return layers_to_delete

# shift layer down to required layer
def shift_layer_down(dict_layers, key, units) -> None:
    if(units <= 0):
     return

    blocks = dict_layers[key]
    dict_layers.pop(key)
    dict_layers.update({key + (gb.grid_square_size * units): blocks})
    for block in blocks:
        block.add_to_pos(0, (gb.grid_square_size * units))


# TODO: not used
def shift_layers_down_offset(dict_layers, keys: list, keys_offset: int):
    # loop to increment each key to the next value
    # save layer, pop it, modify key, then re-add
    for i in range(keys_offset, len(keys), 1):
        blocks = dict_layers[keys[i]]
        dict_layers.pop(keys[i])
        dict_layers.update({keys[i] + gb.grid_square_size: blocks})
    for block in blocks:
        block.add_to_pos(0, (gb.grid_square_size))


# TODO: not used
# shift entire layers down once
def shift_layers_down_once(dict_layers) -> None:
    # get the keys in sorted-reversed order to start from the highest-key
    # highest-key is incremented first, then lower etc
    # if we dont start from highest, then increasing key from lowest to the next layer
    # would overlap keys and so dictionary lookup will be invalid (duplicates)
    keys = list(dict_layers.keys())
    keys.sort(reverse = True)

    # loop to increment each key to the next value
    # save layer, pop it, modify key, then re-add
    for key in keys:
        blocks = dict_layers[key]
        dict_layers.pop(key)
        dict_layers.update({key + gb.grid_square_size: blocks})
    for block in blocks:
        block.add_to_pos(0, (gb.grid_square_size))


# create and re-add the popped layers
def add_missing_layers() -> None:
        keys = list(all_layers.keys())
        keys.sort()
        keys.reverse()
        counter_1 = 0
        for i in range(gb.grid_num_of_vt_squares - len(keys) - 1, -1, -1):#TODO: +10 for extra above
            single_layer = {i * gb.grid_square_size + gb.grid_offset_y: []}
            all_layers.update(single_layer)
            counter_1 += 1


# update scores
def update_player_scores(num_rows_cleared) -> None:
    global temp_rows_cleared_counter

    gb.player_score += (gb.row_cleared_points * num_rows_cleared) + (gb.multi_row_bonus * (num_rows_cleared - 1))
    gb.layers_cleared += num_rows_cleared
    gb.player_level = gb.layers_cleared % 5
    temp_rows_cleared_counter += num_rows_cleared

    if(gb.layers_cleared < 50 and temp_rows_cleared_counter >= 1):
        temp_rows_cleared_counter = 0
        increase_move_speed_by(player_shape, gb.game_speed_increment)


# TODO: parameter current_shape isn't used. Also separate this function into sub-functions
# TODO: maybe it'll be better if this returned layers_to_delete.
# shape collided with bottom-wall
def shape_touched_down(current_shape: TetriminoShape) -> bool:
    global player_shape
    global player_next_shape

    scores_updated = False

    #pygame.display.set_caption("touch down")

    # make it stop moving
    player_shape.moving = False
    
    # player not controlling now so add it to list to be drawn with others
    game_shapes.append(player_shape)

    #------------------------
    # check if shape has touched the top, then its game-over
    for block in player_shape.blocks:
        if( block.shape[1] <= 0 ):
            # TODO: this shouldn't be here
            # this function should return a tuple containing more details
            gb.game_over = True
            return False
    #------------------------

    #-------------------------------------------------------
    # add current shape's blocks to the corresponding layers
    for block in player_shape.blocks:
        # find layer by using the 'y' value as key
        layer = all_layers.get(block.shape[1])
        layer.append(block)
    #-------------------------------------------------------

    # get rows that have been filled
    layers_to_delete = get_completed_rows()
    layers_to_delete.sort(reverse = True)

    # if rows are complete then remove and push others down
    if( len(layers_to_delete) > 0):
        #update scores
        update_player_scores(len(layers_to_delete))
        scores_updated = True

        #----------------------------------------------------
        #store a copy of layers list to reconstruct after removing completed layers (rows)
        keys = list(all_layers.keys())
        keys.sort(reverse = True)

        # remove completed layers
        remove_layers(all_layers, layers_to_delete)

        # get all_layers latest keys after removing some
        adjusted_layer_keys = list(all_layers.keys())
        adjusted_layer_keys.sort(reverse = True)
        
        # loop through layers pushing them down
        for i in range(len(adjusted_layer_keys)):
            # if reference-layer (keys[i]) is below real-layer (adjusted_layer_keys[i]),
            # then push real-layer down to match it
            if(keys[i] > adjusted_layer_keys[i]):
                shift_layer_down(all_layers, adjusted_layer_keys[i],
                                 (keys[i] - adjusted_layer_keys[i]) / gb.grid_square_size)

        # add the missing top layers
        add_missing_layers()
        #---------------------------------------------------

    # switch current-shape to the displayed next-shape
    player_shape = get_new_shape_by_name(player_next_shape.desc)

    # get new next shape
    player_next_shape = setup_next_shape(get_next_random_shape())

    # TODO: take this somewhere else
    # update bounding box and top-points
    update_bounding_box(player_shape)
    update_top_points(player_shape)

    return scores_updated


# calculates the points where the moving shape is dropping
def find_shapepoints_at_bottom(grid_layers, moving_shape: TetriminoShape) -> TetriminoShape:
    
    # list to store found points
    found_points = []   

    # if there are shapes landed..
    if(len(game_shapes) > 0):

        # then loop through all shapes seeing if there are any below/above it
        for blocks in moving_shape.blocks:
            for row_key in grid_layers.keys():
                for cell in grid_layers.get(row_key):
                    if(blocks.shape[0] == cell.shape[0]):
                        # if found then add it to found_points
                        found_points.append(cell.shape)
    
    # (an easy way) add the bottom wall's corresponding-edge-points to the list
    # if there are any blocks on it, then these points will be filtered out anyway, 
    #  else bottom-wall is empty
    for blocks in moving_shape.blocks:
        found_points.append([blocks.shape[0], gb.grid_height + gb.grid_square_size_half])

    # send the points and filter which ones are on top
    found_points = get_points_on_top(found_points, -gb.grid_square_size_half)

    # return what is found
    return found_points

# updates the top_pts
def update_top_points(moving_shape: TetriminoShape):
    global top_pts

    top_pts = find_shapepoints_at_bottom(all_layers, moving_shape)

# updates the bounding-box
def update_bounding_box(moving_shape: TetriminoShape):
    global bounding_box

    bounding_box = moving_shape.update_bounding_box()


# move shape left one block
def move_shape_left_once(shape: TetriminoShape):
    return move_shape_by_one("left", shape, grid_walls, "left-wall")

# move shape right one block
def move_shape_right_once(shape: TetriminoShape):
    return move_shape_by_one("right", shape, grid_walls, "right-wall")

# move shape down one block
def move_shape_down_once(shape: TetriminoShape) -> bool:
    result = move_shape_by_one("down", shape, grid_walls, "bottom-wall")
    if(result[0] == False):
        return shape_touched_down(shape)
    return False

# move shape up one block
def move_shape_up_once(shape: TetriminoShape):
    return move_shape_by_one("up", shape, grid_walls, "bottom-wall")


# rotate shape clockwise if possible
def rotate_shape_cw(shape: TetriminoShape, degrees = 90):
    # return if rotation would collide with a wall
    if shape.check_rotation_collision(shape.blocks[shape.rotation_index].shape, degrees, None, grid_walls, gb.grid_block_distance):
        return
    
    # return if rotation would collide with other shapes
    for landed_shape in game_shapes:
        if shape.check_rotation_collision(shape.blocks[shape.rotation_index].shape, degrees, landed_shape, None, gb.grid_block_distance):
            break
    
    else:# have enough space so do the rotation
        shape.rotate(shape.blocks[shape.rotation_index].shape, 90)
        
        # update bouding-box and top-points
        update_bounding_box(shape)
        update_top_points(shape)


# increases speed to max
def set_speed_max(shape: TetriminoShape):   
    global auto_move_interval
    global auto_move_interval_actual
    global auto_move_interval_fast

    auto_move_interval_actual = auto_move_interval_fast


# increases speed to max
def set_speed_to_normal(shape: TetriminoShape):   
    global auto_move_interval
    global auto_move_interval_actual
    global auto_move_interval_fast

    auto_move_interval_actual = auto_move_interval


# increases the overall game speed
def increase_move_speed_by(shape: TetriminoShape, speed: int):
    global auto_move_interval
    global auto_move_interval_actual
    global auto_move_interval_fast

    auto_move_interval.set_interval(auto_move_interval.interval - speed)
    auto_move_interval_fast.set_interval(auto_move_interval_fast.interval - speed)


# slows down the overall game speed
def decrease_move_speed_by(shape: TetriminoShape, speed: int):
    global auto_move_interval
    global auto_move_interval_actual
    global auto_move_interval_fast

    #auto_move_interval_temp.set_interval(auto_move_interval.interval)
    auto_move_interval.set_interval(auto_move_interval.interval + speed)
    auto_move_interval_fast.set_interval(auto_move_interval_fast.interval + speed)

# skip the menu
def skip_menu(*args):
    global in_menu

    in_menu = False


# TODO: this should be in its own file.
# TODO: problem: how would this file's functions be called from InputProcessor's file?
#------------------------------------------
class InputProcessor:
    def __init__(self) -> None:
        self.key_down_delegates = {
            pygame.K_LEFT:    move_shape_left_once,
            pygame.K_UP:      move_shape_up_once,
            pygame.K_RIGHT:   move_shape_right_once,
            pygame.K_DOWN:    move_shape_down_once,
            pygame.K_r:       rotate_shape_cw,
            pygame.K_RSHIFT:  rotate_shape_cw,
            pygame.K_SPACE:   set_speed_max,
            pygame.K_RETURN:  skip_menu}
        
        self.key_up_delegates = {
            pygame.K_RETURN:  set_speed_to_normal}
    
    def get_delegate_keydown(self, key_pressed):
        return self.key_down_delegates.get(key_pressed, None)
    
    def get_delegate_keyup(self, key_released):
        return self.key_up_delegates.get(key_released, None)
#-------------------------------------------

# TODO: move this somewhere else
input_processor = InputProcessor()
#---------------------

#-------------------------------------------
# processing inputs
def process_inputs():
    global in_menu
    global running

    # loop through input-events
    for event in pygame.event.get():

        # Did the user click the window close button?
        if event.type == pygame.QUIT:
            in_menu = False
            running = False

        # if game is not over
        elif(gb.game_over == False):

            # check for key-down
            if event.type == pygame.KEYDOWN:
    
                # get function delegate and call it
                fn = input_processor.get_delegate_keydown(event.key)
                if( fn != None ):
                    fn(player_shape)


            # check for key-up
            elif event.type == pygame.KEYUP:

                # get function delegate and call it
                fn = input_processor.get_delegate_keyup(event.key)
                if( fn != None ):
                    fn(player_shape)
#-------------------------------------------


#-------------------------------------------
title_logo = pygame.image.load("images/title.png")
scale = (gb.screen_width / title_logo.get_width()) / 1.5

title_logo_rc = [0, 0, 
                int(scale * title_logo.get_width()), int(scale * title_logo.get_height())]
title_rect: pygame.Rect = pygame.Rect(title_logo_rc)
title_rect.move_ip(gb.screen_width / 2 - title_rect.width / 2,
                   25)
title_logo = pygame.transform.scale(title_logo, title_rect.size)
#-------------------------------------------

# menu loop
while in_menu:
     # set frame-rate and store time-elapsed since last frame
    time_passed += clock.tick(60)

    # process inputs
    process_inputs()

    # Fill the background
    screen.fill(gb.grid_bk_colour)

    # draw title
    screen.blit(title_logo, title_rect)
    
     # Flip the display
    pygame.display.flip()
#-------------------------------------------

# reset it so behaves consistent everytime
time_passed = 0
#---------------------

# main loop
while running:

    # set frame-rate and store time-elapsed since last frame
    time_passed += clock.tick(60)

    # process inputs
    process_inputs()

    # Fill the background
    screen.fill(gb.grid_bk_colour)
    
    # draw left box
    pygame.draw.rect(screen, [60,60,60], gb.infobox_rect, gb.border_thickness)
    
    # draw grid-box
    pygame.draw.rect(screen, "black", gb.grid_rect, gb.border_thickness)

    # draw grid lines
    grid.draw_grid(pygame, screen)

    # draw 'next shape'
    draw_shape(player_next_shape)

    #--------------------------------------------------------------
    if(gb.game_over == False):
        if( time_passed >= auto_move_interval_actual.interval ):

            time_passed = 0

            if player_shape.moving == True:
                result = move_shape_down_once(player_shape)
                if( result == True ):
                    score_board.update_scores_texts(gb.player_score, gb.layers_cleared)
    #--------------------------------------------------------------

    # draw texts
    score_board.draw_texts(screen)

    # draw the moving one
    draw_shape(player_shape)

    # draw the rest of the shapes
    for game_shape in game_shapes:
        draw_shape(game_shape)
    
    # draw bounding box
    if(draw_bounding_box != False and bounding_box != None):
        pygame.draw.rect(screen, gb.bounding_box_colour, bounding_box, 1)
    
    # draw top points
    if( top_pts != None):
        for points in top_pts:
            pygame.draw.circle(screen, gb.top_pts_colour, points, gb.top_pts_size, 3)
            # pygame.draw.rect(screen, gb.top_pts_colour, 
            #                  [points[0], points[1], gb.grid_cel_rect[2], gb.grid_cel_rect[3]], 
            #                  gb.top_pts_size, 3)

    # draw game-over
    if( gb.game_over == True ):
        screen.blit(game_over_surface, gb.game_over_xy)

    # Flip the display
    pygame.display.flip()
#--------------------------------------------------------------

# Done! Time to quit.
pygame.quit()
