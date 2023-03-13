import math
from TetrimonoDot import TetriminoDot
from Globals import Globals
from Collisions import Collision

gb = Globals

class TetriminoShape():
    def __init__(self) -> None:
        self.blocks: TetriminoDot = []
        self.colour = "dark blue"
        self.moving = True
        self.desc = "none"
        self.rotation_index: int = 0
        self.box = None # bounding-box coords
    
    # sets the shape for this object
    def set_shape(self, shape_points):
        self.blocks: TetriminoDot = []
        for single_block in shape_points:
             self.blocks.append(TetriminoDot(single_block[0], single_block[1]))
    
    # remove block from self.blocks
    def remove_block(self, block: TetriminoDot) -> bool:
        for i in range(len(self.blocks)):
            if( self.blocks[i] == block ):
                try:
                    self.blocks.remove(block)
                    return True
                except ValueError:
                    return False

    #TODO: not useful as it sets all of the objects x,y to the same value (overlapping)
    def set_pos(self, x: float, y: float):
        for i in range(len(self.blocks)):
            self.blocks[i].shape[0] = x
            self.blocks[i].shape[1] = y
    
    # set position for all of the blocks, using thier previous offset
    def set_pos(self, x: float, y: float, block_spacing):
        for i in range(len(self.blocks)):
            self.blocks[i].shape[0] = (self.blocks[i].original[0] * block_spacing) + x
            self.blocks[i].shape[1] = (self.blocks[i].original[1] * block_spacing) + y
    
    # add to current position
    def add_to_pos(self, x, y):
        for b in self.blocks:
            b.add_to_pos(x, y)

    # rotation in degrees along the point origin_xy
    def rotate(self, origin_xy: float, degrees: float):
        r = math.radians(degrees)
        for block in self.blocks:
            px =  origin_xy[0]
            py = origin_xy[1]
            new_x = (block.shape[0]-px) * (math.cos(r)) - (block.shape[1]-py) * (math.sin(r))
            new_y = (block.shape[0]-px) * (math.sin(r)) + (block.shape[1]-py) * (math.cos(r))
            block.shape[0] = new_x + px
            block.shape[1] = new_y + py

    # sets the colour for all blocks
    def set_colour(self, colour):
        for b in self.blocks:
            b.colour = colour
        self.colour = colour

    # check if this shape (any block) is colliding with colliding_object
    def check_collision(self, col_direction: str, colliding_object: TetriminoDot, collision_spacing: float):
        for b in self.blocks:
            result = b.check_collision(col_direction, colliding_object, collision_spacing)
            if(result[0] == True):
                return result
        return ([False, "none"])
    
    # check this shape's collision with another shape.
    # takes a block from colliding_shape, then sends it to function above (check_collision())
    def check_collision_with_shape(self, col_direction, colliding_shape, collision_spacing: float):
        for b in colliding_shape.blocks:
            result = self.check_collision(col_direction, b, collision_spacing)
            if(result[0] == True):
                return result
        return ([False, "none"])
    
    
    # check if shapes's blocks are on top of any other shape
    # takes each block of this shape and checks collision with each of the other shape's blocks
    def check_exact_collision(self, colliding_shape) -> bool:
        for block in self.blocks:
            for other_block in colliding_shape.blocks:
                if (block.check_exact_collision(other_block)):
                    # two blocks are on top of each other
                    return True
        # no blocks are on top of each other
        else:
            return False
    
    # check for collision with walls
    def check_wall_collision(self, walls, collision_spacing) -> bool:
        for block in self.blocks:
            for wall in walls:
                result = block.check_collision_with_wall(wall, collision_spacing)
                if(result[0] == True):
                    return result[0]
        else:
            return False
    
    # check if this shape can rotate without colliding with other_shape or walls
    def check_rotation_collision(self,origin_xy, degrees: float, other_shape, walls, collision_spacing) -> bool:
        # rotate to check for collition
        self.rotate(origin_xy, degrees)

        # check if there is space to rotate
        result = False
        result2 = False

        if( other_shape != None ):
            result = self.check_exact_collision(other_shape)
            
        if( walls != None):
            result2 = self.check_wall_collision(walls, 0)

        # rotate back to original orientation
        self.rotate(origin_xy, -degrees)

        # return result: 'True' = collided so not rotatable
        #                'False' = not collided so can rotate
        return result | result2
    

    def get_bounding_box(self):
        # get all blocks coords into one list (2D)
        a = [[j for j in i.shape] for i in self.blocks]

        # sort list based on [0] (x-value coord)
        # gets left x
        a.sort(key = lambda x: x[0])
        x1 = a[0][0] - gb.grid_square_size_half

        # sort list based on [0] (x-value coord)
        # gets top y
        a.sort(key = lambda x: x[0], reverse = True)
        x2 = a[0][0] + gb.grid_square_size_half

        # sort list based on [1] (y-value coord)
        # gets right x
        a.sort(key = lambda x: x[1])
        y1 = a[0][1] - gb.grid_square_size_half

        # sort list based on [0] (x-value coord)
        # gets bottom y
        a.sort(key = lambda x: x[1], reverse = True)
        y2 = a[0][1] + gb.grid_square_size_half

        # convert to coords and bounding-box
        return [x1,y1,x2-x1,y2-y1]
    

    # does the same job as above. Leaving it for reference purposes
    def get_bounding_box2(self):
        if(len(self.blocks) <= 2):
           return None
        
        x1 = self.blocks[0].shape[0]
        y1 = self.blocks[0].shape[1] 
        x2 = 0
        y2 = 0

        for i in range(0, len(self.blocks), 1):
            if(self.blocks[i].shape[0] < x1):
                x1 = self.blocks[i].shape[0]
            elif(self.blocks[i].shape[0] > x2):
                x2 = self.blocks[i].shape[0]
            if(self.blocks[i].shape[1] < y1):
                y1 = self.blocks[i].shape[1]
            elif(self.blocks[i].shape[1] > y2):
                y2 = self.blocks[i].shape[1]
        
        x1 -= gb.grid_square_size_half
        x2 += gb.grid_square_size_half
        y1 -= gb.grid_square_size_half
        y2 += gb.grid_square_size_half

        return [x1,y1,x2-x1,y2-y1]
    
    def update_bounding_box(self):
        self.box = self.get_bounding_box()
        return self.box
