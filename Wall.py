


class Wall:
    wall_desc = {"left": "left-wall",
             "right": "right-wall",
             "down": "bottom-wall"}
    
    def __init__(self) -> None:
        self.side = "none"
        self.x = 0
        self.y = 0