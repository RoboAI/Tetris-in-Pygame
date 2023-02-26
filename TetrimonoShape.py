import math
from TetrimonoDot import TetriminoDot

class TetriminoShape():
    def __init__(self) -> None:
        self.blocks: TetriminoDot = []
        self.colour = "dark blue"
        self.moving = True
    
    def set_shape(self, shape_points):
        for single_block in shape_points:
             self.blocks.append(TetriminoDot(single_block[0], single_block[1]))
        
    def set_pos(self, x, y, block_spacing):
        for i in range(len(self.blocks)):
            self.blocks[i].shape[0] = (self.blocks[i].shape[0] * block_spacing) + x
            self.blocks[i].shape[1] = (self.blocks[i].shape[1] * block_spacing) + y
            
    def add_to_pos(self, x, y):
        for b in self.blocks:
            b.add_to_pos(x, y)

    def set_colour(self, colour):
        for b in self.blocks:
            b.colour = colour

    def check_collision(self, col_direction, colliding_object: TetriminoDot, collision_spacing: float):
        for b in self.blocks:
            result = b.check_collision(col_direction, colliding_object, collision_spacing)
            if(result[0] == True):
                return result
        return ([False, "none"])
    
    def check_collision_with_shape(self, col_direction, colliding_shape, collision_spacing: float):
        for b in self.blocks:
            for b2 in colliding_shape.blocks:
                result = b.check_collision(col_direction, b2, collision_spacing)
                if(result[0] == True):
                    return result
        return ([False, "none"])
    
