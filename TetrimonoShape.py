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
    
    def set_shape(self, shape_points):
        self.blocks: TetriminoDot = []
        for single_block in shape_points:
             self.blocks.append(TetriminoDot(single_block[0], single_block[1]))

    #TODO: not useful as it sets all of the objects x,y to the same value (overlapping)
    def set_pos(self, x, y):
        for i in range(len(self.blocks)):
            self.blocks[i].shape[0] = x
            self.blocks[i].shape[1] = y
        
    def set_pos(self, x, y, block_spacing):
        for i in range(len(self.blocks)):
            self.blocks[i].shape[0] = (self.blocks[i].shape[0] * block_spacing) + x
            self.blocks[i].shape[1] = (self.blocks[i].shape[1] * block_spacing) + y
            
    def add_to_pos(self, x, y):
        for b in self.blocks:
            b.add_to_pos(x, y)

    #not working
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
    def check_exact_collision(self, colliding_shape) -> bool:
        for block in self.blocks:
            for other_block in colliding_shape.blocks:
                if (block.check_exact_collision(other_block)):
                    return True
        else:
            return False
    
    
    # check if this shape can rotate without colliding
    def check_rotation_collision(self,origin_xy, degrees: float, other_shape, collision_spacing) -> bool:
        self.rotate(origin_xy, degrees)

        if(self.check_exact_collision(other_shape)):
            self.rotate(origin_xy, -degrees)
            return True

       # for directions in Collision.collisions:
           # result = self.check_collision_with_shape(directions, other_shape, collision_spacing)
           # if(result[0] == True):
             #   self.rotate(origin_xy, -degrees)
              #  return True
        
        self.rotate(origin_xy, -degrees)
        return False