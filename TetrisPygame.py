import pygame
import math

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

def get_angle(p1, p2):
    # Difference in x coordinates
    dx = p2[0] - p1[0]

    # Difference in y coordinates
    dy = p2[1] - p1[1]

    # Angle between p1 and p2 in radians
    theta = math.atan2(dy, -dx)
    
    #convert to degrees
    x = math.degrees(theta)

    pygame.display.set_caption(str(x))

    return x

def get_distance(x1, y1, x2, y2):
    distance = math.sqrt(((x2 - x1) ** 2) + (y2 - y1) ** 2)
    #pygame.display.set_caption(str(distance))
    return distance

def get_distance_from_pts(p1, p2):
    return get_distance(p1[0], p1[1], p2[0], p2[1])


class Tetrimino:
    def __init__(self):
        self.moving: bool = True # used to stop object from moving any further
        self.alive: bool = True # used to destroy this object (e.g. layer complete)
        self.pos: float = [0,0]
        self.shape: float = [[0,0]]

    ### not tested
    #def __init__(self, x: float, y: float) -> None:
        #self.__init__()
        #self.set_pos(self, x, y)

    def set_pos(self, x: float, y: float):
        self.pos[0] = x
        self.pos[1] = y

    def add_to_pos(self, x:float, y:float):
        self.pos[0] += x
        self.pos[1] += y

    def get_bounds(self):
        return self.pos

    def check_collision(self, tetrimino) -> bool:
        others_bounds = tetrimino.get_bounds()
        if(self.pos[0] == others_bounds[0] and self.pos[1] == others_bounds[1]):
            return True
        else:
            return False
    
    # rotate
    def rotate(degrees: int):
        pass

    # object can draw itself
    def draw(self, pygame, screen):
        pass

    # should rotate once. Clockwise if True, Anti-Clockwise if False
    def rotate(self, direction):
        pass


class TetriminoDot(Tetrimino):
    def __init__(self):
        super().__init__()
        self.shape: float = [0,0]
        self.colour = "dark blue"
    
    def __init__(self, x: float, y: float):
        super().__init__()
        self.shape: float = [x, y]

    def set_pos(self, x: float, y: float):
        self.shape[0] = x
        self.shape[1] = y

    def add_to_pos(self, x: float, y: float):
        self.shape[0] += x
        self.shape[1] += y

    def get_bounds(self):
        return [self.shape[0]-1, self.shape[1]-1, 1, 1]
        
    def check_collision(self, col_direction, colliding_object: Tetrimino):
        if(self.shape[0] - colliding_object.shape[0] == 0 and
           self.shape[1] - colliding_object.shape[1] == 0):
            return ([True, "all"])

        angle = get_angle(self.shape, colliding_object.shape)
        distance = get_distance_from_pts(self.shape, colliding_object.shape)
        
        if(distance > grid_block_distance):
            return ([False, "all"])
        
        if(col_direction == "left"):
            if(angle == 0):
                return ([True, col_direction])
        
        elif(col_direction == "right"):
            if(angle == 180):
                return ([True, col_direction])
                
        elif(col_direction == "down"):
            if(angle == 90):
                return ([True, col_direction])
            
        elif(col_direction == "up"):
            if(angle == -90):
                return ([True, col_direction])

        return ([False, "none"])
        

class TetriminoBlock(Tetrimino):
    def __init__(self):
        super().__init__()
        self.shape = [[]]
        
    # set pos to be placed on the grid
    def set_pos(self, x: float, y: float):
        super().set_pos(x, y)
        for i in range(len(self.shape)):
            self.shape[i][0] = (self.shape[i][0] * grid_square_size) + x
            self.shape[i][1] = (self.shape[i][1] * grid_square_size) + y
            
    # add x and y to their respective coordinates
    def add_to_pos(self, x: float, y: float):
        super().add_to_pos(x, y)
        for coords in self.shape:
            coords[0] += x
            coords[1] += y

    #not working
    def rotate(self, degrees: int):
        abc = grid_rect[0] + (grid_square_size / 2) + 1
        for coords in self.shape:
            new_x = (((coords[0] / grid_square_size) - abc) * math.cos(degrees)) - (((coords[1] / grid_square_size) - abc) * math.sin(degrees))
            new_y = (((coords[1] / grid_square_size) - abc) * math.cos(degrees)) + (((coords[0] / grid_square_size) - abc) * math.sin(degrees))
            coords[0] = new_x
            coords[1] = new_y

    def get_bounds(self):
        return [self.shape[0]-1, self.shape[1]-1, 1, 1]

    def check_collision(self, dot: Tetrimino) -> bool:
        others_bounds = dot.get_bounds()
        if (others_bounds[0] <= self.shape[0] and self.shape[0] <= (others_bounds[0] + others_bounds[2]) and 
            others_bounds[1] <= self.shape[1] and self.shape[1] <= (others_bounds[1] + others_bounds[3])):
            return True
        else:
            return False


class TetriminoShape():
    def __init__(self) -> None:
        self.blocks: TetriminoDot = []
        self.colour = "dark blue"
        self.moving = True
    
    def set_shape(self, shape_points):
        for single_block in shape_points:
             self.blocks.append(TetriminoDot(single_block[0], single_block[1]))
        
    def set_pos(self, x, y):
        for i in range(len(self.blocks)):
            self.blocks[i].shape[0] = (self.blocks[i].shape[0] * grid_square_size) + x
            self.blocks[i].shape[1] = (self.blocks[i].shape[1] * grid_square_size) + y
            
    def add_to_pos(self, x, y):
        for b in self.blocks:
            b.add_to_pos(x, y)

    def set_colour(self, colour):
        for b in self.blocks:
            b.colour = colour

    def check_collision(self, col_direction, colliding_object: TetriminoDot):
        for b in self.blocks:
            result = b.check_collision(col_direction, colliding_object)
            if(result[0] == True):
                return result
        return ([False, "none"])
    
    def check_collision_with_shape(self, col_direction, colliding_shape):
        for b in self.blocks:
            for b2 in colliding_shape.blocks:
                result = b.check_collision(col_direction, b2)
                if(result[0] == True):
                    return result
        return ([False, "none"])
    

        
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
#-----------------
I_block = TetriminoShape()
I_block.set_shape(IBlock.copy())
I_block.set_pos(grid_offset_x, grid_offset_y)
I_block.add_to_pos(grid_square_size * 6, grid_square_size * 7)
I_block.set_colour("red")
#-----------------
T_block = TetriminoShape()
T_block.set_shape(TBlock.copy())
T_block.set_pos(grid_offset_x, grid_offset_y)
T_block.add_to_pos(grid_square_size * 4, grid_square_size)
T_block.set_colour("dark blue")
#-----------------
L_block = TetriminoShape()
L_block.set_shape(LBlock.copy())
L_block.set_pos(grid_offset_x, grid_offset_y)
L_block.add_to_pos(grid_square_size * 2, grid_square_size * 7)
L_block.set_colour("dark green")
#-----------------
Z_block = TetriminoShape()
Z_block.set_shape(ZBlock.copy())
Z_block.set_pos(grid_offset_x, grid_offset_y)
Z_block.add_to_pos(grid_square_size * 6, grid_square_size * 12)
Z_block.set_colour("dark orange")
#-----------------
moving_dot = T_block
single_dot = I_block
game_shapes = [I_block, L_block, Z_block]



def draw_shape(tetri_blocks: TetriminoShape):
    for block in tetri_blocks.blocks:
        pygame.draw.circle(screen, block.colour, block.shape, 10, 10)
    

def move_shape_by_one(direction, shape: TetriminoShape):
    for single_shape in game_shapes:
        result = moving_dot.check_collision_with_shape(direction, single_shape)
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