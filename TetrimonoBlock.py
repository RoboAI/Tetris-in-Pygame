#####
#####class not used. can delete
#####

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

