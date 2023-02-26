from Tetrimino import Tetrimino
from MyFunctions import get_angle, get_distance, get_distance_from_pts
from Collisions import Collision

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
        
    def check_collision(self, col_direction, colliding_object: Tetrimino, collision_spacing):
        # if somehow the shapes are on top of each other then just return 'collided all sides'
        if(self.shape[0] - colliding_object.shape[0] == 0 and
           self.shape[1] - colliding_object.shape[1] == 0):
            return ([True, "all"])

        # get and distance between the two objects
        angle = get_angle(self.shape, colliding_object.shape)
        distance = get_distance_from_pts(self.shape, colliding_object.shape)
        
        #if there is a gap of more than one-block, then there is no collision
        if(distance > collision_spacing):
            return ([False, "none"])

        # if objects are next to each other, then return 'True and direction of collision'
        if(col_direction, angle) in Collision.collisions.items():
            return ([True, col_direction]) 

        return ([False, "none"])
        
    