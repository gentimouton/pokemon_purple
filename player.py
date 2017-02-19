from character import Character

class Player(Character):
    def __init__(self, frames, containers, pos=(1, 1)):
        Character.__init__(self, frames, containers, pos)
        
