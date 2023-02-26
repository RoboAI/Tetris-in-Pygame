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
        super().__init__(self)
        self.shape: float = [0,0]
    
    def __init__(self, x: float, y: float):
        super().__init__(self)
        self.shape: float = [x, y]

    def get_bounds(self):
        return [self.shape[0]-1, self.shape[1]-1, 1, 1]

    def check_collision(self, dot: Tetrimino) -> bool:
        others_bounds = dot.get_bounds()
        if (others_bounds[0] <= self.shape[0] and self.shape[0] <= (others_bounds[0] + others_bounds[2]) and 
            others_bounds[1] <= self.shape[1] and self.shape[1] <= (others_bounds[1] + others_bounds[3])):
            return True
        else:
            return False
        
    def check_collision(self, col_direction, colliding_object: Tetrimino):
        if( col_direction == "down" ):
            if(colliding_object.shape[1] - self.shape[1] <= grid_square_size):
                return ([True, col_direction])
            
        elif ( col_direction == "right" ):
            if( colliding_object.shape[0] - self.shape[0] ):
                return ([True, col_direction])
            
        elif ( col_direction == "left" ):
            if( self.shape[0] - colliding_object.shape[0] ):
                return ([True, col_direction])
            
        else:
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


class IBlock(TetriminoBlock):
    def __init__(self):
        super().__init__()
        self.shape = [[0,0],[1,0],[2,0],[3,0],[4,0]]

class TetriminoShape():
    def __init__(self) -> None:
        self.blocks: TetriminoDot = []
    
    def set_shape(self, shape_points):
        for single_block in shape_points:
             self.blocks.append(TetriminoDot(single_block[0], single_block[1]))
        
    def set_pos(self, x, y):
        for b in self.blocks:
            b.set_pos(x, y)
            
    def add_to_pos(self, x, y):
        for b in self.blocks:
            b.add_to_pos(x, y)
    

    def check_collision(self, colliding_object: TetriminoDot):
        for b in self.blocks:
            b = TetriminoDot()#####
            if b.check_collision(colliding_object):
                

                return b
    
    

#class TheGame(SingleDot):
    #def __init__(self):
        
class SingleSquare:
    def __init__(self):
        self.x_pos: float = 0
        self.y_pos: float = 0
        self.rect = [0,0,0,0]

    def move_me(self, x:float, y:float):
        self.rect[0] += x
        self.rect[1] += y


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

# time calculator for shapes movement interval
shapes_tick_interval = 500 # in milliseconds; move shape every xxx milliseconds

# Set up the drawing window
screen = pygame.display.set_mode([screen_width, screen_height])

counter = 0
time_passed = 0

# Get the Clock to limit frame-rate
clock = pygame.time.Clock()

# Run until the user asks to quit
running = True

single_box = SingleSquare()
single_box.rect = [grid_rect[0], 0, grid_square_size, grid_square_size]
#-----------------
single_dot = Tetrimino()
single_dot.set_pos( grid_rect[0] + (grid_square_size / 2) + 1,
                    grid_rect[1] + (grid_square_size / 2) + 1)
single_dot.add_to_pos(grid_square_size * 5, grid_square_size * 5)
#------------------
moving_dot = Tetrimino()
moving_dot.set_pos( grid_rect[0] + (grid_square_size / 2) + 1,
                    grid_rect[1] + (grid_square_size / 2) + 1)
moving_dot.add_to_pos(grid_square_size, grid_square_size)
#------------------
i_block = IBlock()
i_block.set_pos(grid_rect[0] + (grid_square_size / 2) + 1,
                grid_rect[1] + (grid_square_size / 2) + 1)
#-----------------

counter2 = 0
while running:
    # set frame-rate
    time_passed += clock.tick(60)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    
    pygame.draw.rect(screen, "green", infobox_rect, border_thickness)
    pygame.draw.rect(screen, "red", grid_rect, border_thickness)

    draw_grid(single_box.y_pos)

    #--------------------------------------------------------------
    if time_passed >= shapes_tick_interval :
        #pygame.display.set_caption(str(time_passed))
        time_passed = 0

        #pygame.display.set_caption(str(grid_square_size))

        if moving_dot.moving == True:
            # do a dummy move to check for collision
            moving_dot.add_to_pos(grid_square_size, grid_square_size)

            # if colliding..
            if moving_dot.check_collision(single_dot):
                #stop object
                moving_dot.moving = False
                # move the object back to its previous point
                moving_dot.add_to_pos(-grid_square_size, -grid_square_size)
                pygame.display.set_caption("Collided!! ")
        
        
    #--------------------------------------------------------------

    #pygame.draw.rect(screen, "dark green", single_box.rect, 100)
    pygame.draw.circle(screen, "blue", single_dot.pos, 3, 1)
    pygame.draw.circle(screen, "blue", moving_dot.pos, 3, 1)
    #for box in i_block.shape:
        #pygame.draw.circle(screen, "blue", box, 2)

    # Flip the display
    pygame.display.flip()

    counter += 1

# Done! Time to quit.
pygame.quit()