
# time calculator for shapes movement interval
class AutoDownMoveInterval:
    def __init__(self, interval: int, min_interval: int) -> None:
        self.interval = interval # in milliseconds; move shape every xxx milliseconds
        self.min = min_interval
        self.set_interval(interval)
    
    def set_interval(self, interval):
        if(interval < self.min):
            self.interval = self.min
        else:
            self.interval = interval