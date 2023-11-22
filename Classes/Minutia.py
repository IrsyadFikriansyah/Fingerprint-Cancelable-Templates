class Minutia:
    def __init__(self, x, y, rad, type, is_selected=False) -> None:
        self.x = x
        self.y = y
        self.rad = rad
        self.type = type
        self.is_selected = is_selected
        self.neighbors = []