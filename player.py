from character import Character


class Player(Character):
    def __init__(self, level, frames, containers, pos=(1, 1)):
        Character.__init__(self, level, frames, containers, pos)
        self.base_move_speed = 5 # cells per second

