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
    
    def set_shape(self, shape_points):
        self.blocks: TetriminoDot = []
        for single_block in shape_points:
             self.blocks.append(TetriminoDot(single_block[0], single_block[1]))
    
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
            self.blocks[i].shape[0] = (self.blocks[i].shape[0] * block_spacing) + x
            self.blocks[i].shape[1] = (self.blocks[i].shape[1] * block_spacing) + y
            
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
        result = self.check_exact_collision(other_shape)
        result2 = self.check_wall_collision(walls, 0)

        # rotate back to original orientation
        self.rotate(origin_xy, -degrees)

        # return result: 'True' = collided so not rotatable
        #                'False' = not collided so can rotate
        return result | result2
