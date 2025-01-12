
class Directions :
    def __init__(self)-> None: 
        self.Directions = {
            'LEFT': (0, -1),
            'RIGHT': (0, 1),
            'DOWN': (1, 0),
            'UP': (-1, 0)
            }
        
    def Return_Directions(self) :
        return self.Directions