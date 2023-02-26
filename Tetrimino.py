
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
