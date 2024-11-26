
class Square_In_State:

    def __init__(self , x , y , new_x , new_y , type , prev_type , Role , target_square , In_Place )-> None:
        self.x = x
        self.y = y
        self.type = type
        self.prev_type = prev_type
        self.target_square = target_square
        self.Role = Role
        self.new_y = new_y
        self.new_x = new_x
        self.In_Place = In_Place
 
    def __str__(self)-> str:
        if self.type == "Black":
            return '⬛'     
        elif self.type == "White":
            return '⬜'        
        elif self.type == 'Red':
            return '🟥'        
        elif self.type == 'Blue':
            return '🟦'      
        elif self.type == 'Yellow': 
            return '🟨'
        elif self.type == 'Green':
            return '🟩'       
        elif self.type == 'Orange':
            return '🟧'               
        elif self.type == 'RedGoal':
           return '🔴' 
        elif self.type == 'OrangeGoal':
           return '🟠'
        elif self.type == 'BlueGoal':
           return '🔵'
        elif self.type == 'YellowGoal':
           return '🟡' 
        elif self.type == 'GreenGoal':
           return '🟢'        
        elif self.type == 'BlackWhite':
           return '🔲' 
        elif self.type == 'WhiteWhite':
           return '🔳' 

    def __eq__(self, other):
        if not isinstance(other, Square_In_State):
            return False
        return (
            self.x == other.x and
            self.y == other.y and
            self.new_x == other.new_x and
            self.new_y == other.new_y and
            self.type == other.type and
            self.prev_type == other.prev_type and
            self.Role == other.Role and
            self.target_square == other.target_square and
            self.In_Place == other.In_Place
        )
        
    def __hash__(self):
        return hash((self.x , self.y ,
                      self.new_x , self.new_y ,
                          self.type , self.prev_type ,
                            self.Role , self.target_square , self.In_Place))

