from character import Character

class Player(Character):
    def __init__(self, level, frames, containers, pos=(1, 1)):
        Character.__init__(self, level, frames, containers, pos)
        self.move_speed = 1.0 / 4


        
