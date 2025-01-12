
from copy import deepcopy
from Directions import Directions
import copy

class State:
    def __init__(self,rows,cols,board)-> None:
        self.rows = rows
        self.cols = cols
        self.board = board
        self.Players_List  = self.Get_All_Players()
        self.Parent = None
        self.cost = 0
        self.Manhattan_Distance_Hurestic = 0
        self.A_Star_Hurestic = 0

    def copy(self):
        new_board = [[square.copy() for square in row] for row in self.board]
        new_state = State(self.rows, self.cols, new_board)
        new_state.Parent = self.Parent
        new_state.cost = self.cost
        new_state.A_Star_Hurestic = self.A_Star_Hurestic
        new_state.Manhattan_Distance_Hurestic = self.Manhattan_Distance_Hurestic
        new_state.x = self.rows
        new_state.y = self.cols 
        return new_state 

    # def __lt__(self, other):
    #     return self.A_Star_Hurestic < other.A_Star_Hurestic 
    
    def __lt__(self, other):
        return self.cost < other.cost 

    def Get_Variable_Square(self):
        for row in self.board:
            for square in row:
                if square.type == 'WhiteWhite' :
                    return square
                    
    def Get_Manhattan_Distance_Hurestic (self) :
        Player_List = self.Get_All_Players()
        Manhattan_Distance_List = []
        for square in Player_List :
            Target = self.Get_Target_Square(square.target_square)
            if(Target == None) :
                Target = self.Get_Variable_Square()
            Manhattan_Distance_Hurestic = abs(square.x - Target.x) + abs(square.y - Target.y)
            Manhattan_Distance_List.append(Manhattan_Distance_Hurestic)
        Manhattan_Distance = 0
        for Hurestic in Manhattan_Distance_List :
            Manhattan_Distance = Manhattan_Distance + Hurestic
        self.Manhattan_Distance_Hurestic = Manhattan_Distance
            
    def __str__(self)-> str:
        result = ""
        for row in self.board:
            for square in row:
                result += str(square)
            result += '\n'
        return result

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.board == other.board)

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def Check_If_Accept_state(self) :
        Targets = self.Get_All_Targets()
        has_duplicates = any(Targets.count(item) > 1 for item in Targets)
        return has_duplicates
       
    def Get_All_Players(self):
        Players_List = []
        for row in self.board:
            for square in row:
                if square.Role == 'Player' and  square.In_Place == False :
                    Players_List.append(square)

        return Players_List                 
    
    def Get_Target_Square(self , type):
        for row in self.board:
            for square in row:
                if square.prev_type == type:
                    return square

    def getTargetCoordinates(self , type):
        Target_Squares_List = [] 
        for row in self.board:
            for square in row:
                if square.prev_type == type:
                    Target_Squares_List.append(square)
        return Target_Squares_List
                
    def isGoal(self):
        Check_Square_Goal = True
        for Player in self.Players_List :
            if Player.In_Place == False :
                Check_Square_Goal = False
                break

        return Check_Square_Goal
    
    def isLoss(self):
        Check_Square_Loss = False
        for Player in self.Players_List :
            if Player.prev_type == 'BlackWhite' :
                Check_Square_Loss = True
                break

        return Check_Square_Loss

    def change_To_White(self , x , y) :
        self.board[x][y].type = 'White'
        self.board[x][y].Role = 'Crossing'
        self.board[x][y].In_Place = True
        self.board[x][y].target_square = ''
        self.board[x][y].prev_type = 'White'
 
    def change_Variable_Square_To_Goal_Square(self , x , y , target_square) :
        self.board[x][y].type = target_square
        self.board[x][y].Role = 'PlayerGoal'
        self.board[x][y].In_Place = True
        self.board[x][y].target_square = target_square
        self.board[x][y].prev_type = target_square
  
    def change_Previous_Square(self , square):
            # change Previous Square If is Goal To someone Players
            prev_type = self.board[square.x][square.y].prev_type
            if (prev_type == 'BlueGoal' or prev_type == 'RedGoal' 
                or prev_type == 'GreenGoal' or prev_type == 'OrangeGoal' 
                or prev_type == 'YellowGoal') :
                self.board[square.x][square.y].type = prev_type
                self.board[square.x][square.y].Role = 'PlayerGoal'
                self.board[square.x][square.y].In_Place = True
                self.board[square.x][square.y].target_square = prev_type
            # change Previous Square If is White
            if self.board[square.x][square.y].prev_type == 'White':
                self.change_To_White(square.x , square.y)

    def change_Player_Move(self , square):
        if (square.In_Place == True) :
            # change new Player position Square
            self.change_To_White(square.new_x , square.new_y)
        else :
            Type = self.board[square.x][square.y].type
            if (Type == 'GreenYellow') :
                self.board[square.new_x][square.new_y].type = 'Yellow'
            elif (Type == 'OrangeGreen') :
                self.board[square.new_x][square.new_y].type = 'Green'
            else :
                self.board[square.new_x][square.new_y].type = square.type
            self.board[square.new_x][square.new_y].Role = square.Role
            self.board[square.new_x][square.new_y].target_square = square.target_square
            self.board[square.new_x][square.new_y].In_Place = square.In_Place
        # change Previous Square
        self.change_Previous_Square(square)
        square.new_x , square.new_y = 0 , 0
        self.Players_List = self.Get_All_Players()

    def checkMove(self , x , y , square):
        if square.x + x < 0 :
            return False 
        elif square.x + x >= self.rows :
            return False  
        elif square.y + y < 0 :
            return False
        elif square.y + y >= self.cols :
            return False
        elif self.board[square.x + x ][square.y + y].type == "Black":
            return False
        elif self.board[square.x + x ][square.y + y].Role == "Player":
            return False   
        else:
            return True
        
    def Get_All_Targets(self):
        Targets_List = []
        for row in self.board:
            for square in row:
                if (square.prev_type == 'BlueGoal' or square.prev_type == 'RedGoal' 
                or square.prev_type == 'GreenGoal' or square.prev_type == 'OrangeGoal' 
                or square.prev_type == 'YellowGoal') :
                    Targets_List.append(square.prev_type)
        return Targets_List 

    def player_Reach_Target(self , x , y , square):
        Target_Squares_List = self.getTargetCoordinates(square.target_square)
        if (Target_Squares_List) :
            for Target in Target_Squares_List :
                if Target.x == x + square.x and Target.y == y + square.y :
                    square.In_Place = True              
                    return True
            return False

    def player_Reach_To_Loss_Square(self , x , y , square):
            if self.board[square.x + x ][square.y + y].type == 'BlackWhite':
                return True           
            return False

    def player_Reach_To_Variable_Square(self , x , y , square):
            if self.board[square.x + x ][square.y + y].prev_type == 'WhiteWhite':
                return True           
            return False

    def Get_Next_States(self):
        directions = Directions().Return_Directions()
        Next_States = []
        for direction, (dx, dy) in directions.items():
            i = 0
            loss_Square = False
            parent = self.copy()
            Players_can_move = [
                player for player in parent.Players_List 
                if parent.checkMove(dx, dy, player)
                ]
            if not Players_can_move:
                continue
            if direction in ['DOWN', 'RIGHT']:
                Players_can_move.reverse()
            for square in Players_can_move:           
                x, y = 0, 0
                while True:
                    x += dx
                    y += dy   
                    if not parent.checkMove(x, y, square):
                        break    
                    if parent.player_Reach_Target(x, y, square):
                        x, y = x + dx, y + dy
                        i = i + 1
                        break   
                    if parent.player_Reach_To_Loss_Square(x, y, square):
                        loss_Square = True
                        x, y = x + dx, y + dy
                        break   
                    if (parent.player_Reach_To_Variable_Square(x, y, square)) :
                        parent.change_Variable_Square_To_Goal_Square(square.x + x, square.y + y, square.target_square) 
                        # i = i + 1
                    i = i + 1
                new_x, new_y = square.x + x - dx , square.y + y - dy
                square.new_x, square.new_y = new_x, new_y
                parent.change_Player_Move(square) 
            parent.cost = i
            # parent.cost += 5
            if loss_Square == True:
                    parent.cost = 100
                    # continue   
            if parent.Check_If_Accept_state():
                parent.cost = 100
                # continue  
            Next_States.append(parent)  
        return Next_States
 
