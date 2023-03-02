from Wall import Wall
from MyFunctions import get_angle, get_distance, get_distance_from_pts

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
    
    def check_collision_with_wall(self, wall, grid_spacing):
        if(wall[0] == "left-wall"):
            if(self.shape[0] - grid_spacing <= wall[1][0]):
                return ([True, wall[0]])
        elif(wall[0] == "right-wall"):
            if(self.shape[0] + grid_spacing >= wall[1][0]):
                return ([True, wall[0]])
        elif(wall[0] == "bottom-wall"):
            if(self.shape[1] + grid_spacing >= wall[1][1]):
                return ([True, wall[0]])
            
        return ([False, "none"])

    # object can draw itself
    def draw(self, pygame, screen):
        pass

    # should rotate once. Clockwise if True, Anti-Clockwise if False
    def rotate(self, direction):
        pass
