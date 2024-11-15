
from copy import deepcopy
from Directions import Directions

class State:

    def __init__(self,rows,cols,board)-> None:
        self.rows = rows
        self.cols = cols
        self.board = board
        self.Players_List  = self.Get_All_Players()
        self.direction = None
        self.Parent = None
    
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
        return (
            self.rows == other.rows and
            self.cols == other.cols and
            # self.direction == other.direction and
            self.Players_List == other.Players_List and
            self.board == other.board
        )

    def Get_All_Players(self):
        Players_List = []
        for row in self.board:
            for square in row:
                if square.Role == 'Player' and  square.In_Place == False :
                    Players_List.append(square)

        return Players_List
                    
    def getPlayerCoordinates(self):
        for row in self.board:
            for square in row:
                if square.type == 'Red':
                    return square.x , square.y
     
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
                or prev_type == 'YellowGoal' or prev_type == 'YellowGoal') :
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
            # change new Player position Square
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

    def playerReachTarget(self , x , y , square):
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
            if self.board[square.x + x ][square.y + y].type == 'WhiteWhite':
                return True           
            return False

    def Get_Next_States(self):
        directions = Directions()
        Next_States = []
        for direction in directions.Return_Directions() :
                parent = deepcopy(self)

                ########################################################## MOVE UP
                if direction == 'UP':
                    Players_can_move = []
                    for player in parent.Players_List :
                        if(parent.checkMove(-1 , 0 , player)):
                            Players_can_move.append(player)
                        else :
                            continue

                    if Players_can_move == [] :
                        continue                   

                    for square in Players_can_move:                                             
                        x , y = 0 , 0
                        while (True) :
                            x = x - 1 
                            if not parent.checkMove(x , y , square) :
                                break
                            if parent.playerReachTarget(x , y , square) :
                                x = x - 1
                                break
                            if parent.player_Reach_To_Loss_Square(x , y , square) :
                                x = x - 1
                                break
                            if parent.player_Reach_To_Variable_Square(x , y , square) :
                                parent.change_Variable_Square_To_Goal_Square(square.x + x , square.y + y , square.target_square)         
                        new_player_x , new_player_y = square.x + x + 1 , square.y + y
                        square.new_x , square.new_y = new_player_x , new_player_y
                        parent.change_Player_Move(square)
                                      

                ########################################################## MOVE DOWN
                elif direction == 'DOWN':

                    Players_can_move = []
                    for player in parent.Players_List :
                        if(parent.checkMove(1 , 0 , player)):
                            Players_can_move.append(player)
                        else :
                            continue

                    if Players_can_move == [] :
                        continue 
                        
                    Players_can_move.reverse()    
                    for square in Players_can_move:                                                     
                        x , y = 0 , 0
                        while (True) :
                            x = x + 1
                            if not parent.checkMove(x , y , square) :
                                break
                            if parent.playerReachTarget(x , y , square) :
                                x = x + 1
                                break 
                            if parent.player_Reach_To_Loss_Square(x , y , square) :
                                x = x + 1
                                break
                            if parent.player_Reach_To_Variable_Square(x , y , square) :                       
                                parent.change_Variable_Square_To_Goal_Square(square.x + x , square.y + y , square.target_square) 
                        new_player_x , new_player_y = square.x + x - 1 , square.y + y
                        square.new_x , square.new_y = new_player_x , new_player_y
                        parent.change_Player_Move(square)
                                                              
                
                ########################################################## MOVE LEFT
                elif direction == 'LEFT' :

                    Players_can_move = []
                    for player in parent.Players_List :
                        if(parent.checkMove(0 , -1 , player)):
                            Players_can_move.append(player)
                        else :
                            continue   
                      
                    if Players_can_move == [] :
                        continue
                         
                    for square in Players_can_move:                
                        x , y = 0 , 0
                        while (True) :
                            y = y - 1
                            if not parent.checkMove(x , y , square) :
                                break
                            if parent.playerReachTarget(x , y , square) :
                                y = y - 1
                                break
                            if parent.player_Reach_To_Loss_Square(x , y , square) :
                                y = y - 1
                                break
                            if parent.player_Reach_To_Variable_Square(x , y , square) :
                                parent.change_Variable_Square_To_Goal_Square(square.x + x , square.y + y , square.target_square) 
                        new_player_x , new_player_y = square.x + x , square.y + y + 1
                        square.new_x , square.new_y = new_player_x , new_player_y
                        parent.change_Player_Move(square) 
                         

                ########################################################## MOVE RIGHT
                elif direction == 'RIGHT' :

                    Players_can_move = []
                    for player in parent.Players_List :
                        if(parent.checkMove(0 , 1 , player)):
                            Players_can_move.append(player)
                        else :
                            continue  

                    if Players_can_move == [] :
                        continue


                    Players_can_move.reverse()
                    for square in Players_can_move:              
                        x , y = 0 , 0
                        while (True) :
                            y = y + 1
                            if not parent.checkMove(x , y , square) :
                                break
                            if parent.playerReachTarget(x , y , square) :
                                y = y + 1
                                break
                            if parent.player_Reach_To_Loss_Square(x , y , square) :
                                y = y + 1
                                break
                            if parent.player_Reach_To_Variable_Square(x , y , square) :
                                parent.change_Variable_Square_To_Goal_Square(square.x + x , square.y + y , square.target_square) 
                        new_player_x , new_player_y = square.x + x , square.y + y - 1
                        square.new_x , square.new_y = new_player_x , new_player_y
                        parent.change_Player_Move(square)
                     
                parent.direction = direction
                Next_States.append(deepcopy(parent))
    
        return Next_States
                
