

#**************************************Zero_Squares_Game*************************************# 
#********************************************************************************************#


# file name : main.py ********************************************************************
# Main starting point for program implementation
import sys
sys.stdout.reconfigure(encoding='utf-8')
from Zero_Squares_LeveLs import Zero_Squares_LeveLs
from Level_Selection_Menu import Level_Selection_Menu
from Main_Menu_GUI import Main_Menu_GUI

def main():
    Level_Object = Level_Selection_Menu()
    Level_Selected = Level_Object.level_selection_menu() - 1
    init_state = Zero_Squares_LeveLs(Level_Selected).Return_Array_Object()
    print(init_state)
    Game = Main_Menu_GUI()
    Game.main_menu(init_state)
   
if __name__ == '__main__':
    main()


#********************************************************************************************#


# file name : State.py ********************************************************************
# This file contains everything related to the game structure
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
        self.Heuristic_Value = 0

    def copy(self):
        new_board = [[square.copy() for square in row] for row in self.board]
        new_state = State(self.rows, self.cols, new_board)
        new_state.Parent = self.Parent
        new_state.cost = self.cost
        new_state.x = self.rows
        new_state.y = self.cols 
        return new_state 

    def __lt__(self, other):
        return self.cost < other.cost  
    
    
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

    def Get_All_Players(self):
        Players_List = []
        for row in self.board:
            for square in row:
                if square.Role == 'Player' and  square.In_Place == False :
                    Players_List.append(square)

        return Players_List                 
     
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
        
    def Get_All_Targets(self):
        Targets_List = []
        for row in self.board:
            for square in row:
                if square.Role == 'PlayerGoal':
                    Targets_List.append(square)
        return Targets_List 
    
    def Player_without_Targets(self , square) :
        result = True
        Targets = self.Get_All_Targets()
        for Target in Targets :
            if Target.prev_type == square.target_square :
                result = False
                break
        return result

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
            loss_Square = False
            parent = self.copy()
            Players_can_move = [
                player for player in parent.Players_List 
                if parent.checkMove(dx, dy, player)]
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
                        break   
                    if parent.player_Reach_To_Loss_Square(x, y, square):
                        loss_Square = True
                        break 
                    if parent.player_Reach_To_Variable_Square(x, y, square):
                        parent.change_Variable_Square_To_Goal_Square(square.x + x, square.y + y, square.target_square)                    
                if direction == 'UP':
                    new_x, new_y = square.x + x - dx, square.y + y
                elif direction == 'DOWN':
                    new_x, new_y = square.x + x - dx, square.y + y
                elif direction == 'LEFT':
                    new_x, new_y = square.x + x, square.y + y - dy
                else:   
                    new_x, new_y = square.x + x , square.y + y - dy
                square.new_x, square.new_y = new_x, new_y
                parent.change_Player_Move(square) 
            if loss_Square == True:
                    continue   
            parent.cost = 1
            Next_States.append(parent)  
        return Next_States
 

#********************************************************************************************#


# file name : Square_In_State.py ********************************************************************
# This file contains all the properties of the square in the board 
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
    
    def copy(self):
        new_square = Square_In_State(self.x , self.y ,
                                      self.new_x , self.new_y ,
                                        self.type , self.prev_type ,
                                          self.Role , self.target_square ,
                                            self.In_Place)  
        return new_square


#********************************************************************************************#


# file name : Directions.py ********************************************************************
# This file returns the direction Matrix.
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


#********************************************************************************************#


# file name : Depth_First_Search.py ********************************************************************
# for solve the game using DFS
from copy import deepcopy
from Draw_Board_Pygame import Draw_Board_Pygame
import psutil
import time 
import os 

class Depth_First_Search:

    def __init__(self , init_state) -> None:
        self.init_state = init_state
        self.current_state = deepcopy(init_state)
        self.Path_Goal_List = []
        self.visited_States_Number = 0
        self.stack = []
        self.stack.append(init_state)
        self.visited = set()
        self.visited.add(init_state)
        self.Draw = Draw_Board_Pygame()
    
    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        return memory_mb

    def Print_Path_Goal(self , current_state) :
        State_From_Goal_Path = deepcopy(current_state)
        while(State_From_Goal_Path.Parent != None) :
            self.Path_Goal_List.append(State_From_Goal_Path)
            State_From_Goal_Path = State_From_Goal_Path.Parent

        self.Path_Goal_List.append(State_From_Goal_Path)
        self.Path_Goal_List.reverse()
        print("all States That Generated Path are:")
        print('\n')
        for state in self.Path_Goal_List :
            print (state)

        print("the Number States From Init State To Goal State are :")
        Length = len(self.Path_Goal_List)
        print (Length)
        print("the Number States That Visited are :")           
        print (self.visited_States_Number)

    def Get_Time_and_Meomory(self , start_time , initial_memory) :
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Time taken by the algorithm : {execution_time:.2f} ")
        final_memory = self.get_memory_usage()
        memory_used = final_memory - initial_memory
        print(f"Memory Used: {memory_used:.2f} MB")
        print(f"Total Memory Usage: {final_memory:.2f} MB")

    def Depth_First_Search_Solve(self) :
        start_time = time.time()
        initial_memory = self.get_memory_usage()
        while self.stack :
            self.current_state = self.stack.pop()
            if self.current_state.isGoal() :
                self.visited.add(deepcopy(self.current_state))
                print(self.current_state)
                self.Draw.draw_Screen_Game(self.current_state.board)
                print("Gaaaaaaaaaame Oveeeeeeeeeeeer")
                self.Print_Path_Goal(self.current_state)
                self.Get_Time_and_Meomory(start_time , initial_memory)
                return None           
            print(self.current_state)
            self.Draw.draw_Screen_Game(self.current_state.board)  
            Next_States = self.current_state.Get_Next_States()           
            for state in Next_States :               
                if state.isLoss() :
                    continue
                if state not in self.visited :
                    state.Parent = self.current_state
                    self.visited_States_Number += 1 
                    self.visited.add(state)
                    self.stack.append(state)                          
        return None


#********************************************************************************************#


# file name : Breadth_First_Search.py ********************************************************************
# for solve the game using BFS
from copy import deepcopy
from Draw_Board_Pygame import Draw_Board_Pygame
from collections import deque
import psutil
import time 
import os

class Breadth_First_Search:
    
    def __init__(self , init_state) -> None:
        self.init_state = init_state
        self.current_state = deepcopy(init_state)
        self.Path_Goal_List = []
        self.visited_States_Number = 0
        self.queue = deque()
        self.queue.append(init_state)
        self.visited = set()
        self.visited.add(init_state)
        self.Draw = Draw_Board_Pygame()

    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        return memory_mb

    def Print_Path_Goal(self , current_state) :
        State_From_Goal_Path = deepcopy(current_state)
        while(State_From_Goal_Path.Parent != None) :
            self.Path_Goal_List.append(State_From_Goal_Path)
            State_From_Goal_Path = State_From_Goal_Path.Parent

        self.Path_Goal_List.append(State_From_Goal_Path)
        self.Path_Goal_List.reverse()
        print("all States That Generated Path are:")
        print('\n')
        for state in self.Path_Goal_List :
            print (state)

        print("the Number States From Init State To Goal State are :")
        Length = len(self.Path_Goal_List)
        print (Length)
        print("the Number States That Visited are :")           
        print (self.visited_States_Number)

    def Get_Time_and_Meomory(self , start_time , initial_memory) :
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Time taken by the algorithm : {execution_time:.2f} ")
        final_memory = self.get_memory_usage()
        memory_used = final_memory - initial_memory
        print(f"Memory Used: {memory_used:.2f} MB")
        print(f"Total Memory Usage: {final_memory:.2f} MB") 

    def Breadth_First_Search_Solve(self) :
        start_time = time.time()
        initial_memory = self.get_memory_usage()
        while self.queue :
            self.current_state = self.queue.popleft()
            if self.current_state.isGoal() :
                self.visited.add(self.current_state)
                print(self.current_state)
                self.Draw.draw_Screen_Game(self.current_state.board)
                print("Gaaaaaaaaaame Oveeeeeeeeeeeer")
                self.Print_Path_Goal(self.current_state)
                self.Get_Time_and_Meomory(start_time , initial_memory)
                return None        
            print(self.current_state)
            self.Draw.draw_Screen_Game(self.current_state.board) 
            Next_States = self.current_state.Get_Next_States()           
            for state in Next_States :               
                if state.isLoss() :
                    continue
                if state not in self.visited :
                    state.Parent = self.current_state
                    self.visited_States_Number += 1 
                    self.visited.add(state)
                    self.queue.append(state)     
        return None


#********************************************************************************************#


# file name : DFS_By_Recursion.py ********************************************************************
# for solve the game using Recursion DFS
from copy import deepcopy
from Draw_Board_Pygame import Draw_Board_Pygame
import psutil
import time 
import os 

class DFS_By_Recursion:

    def __init__(self) -> None:
        self.Path_Goal_List = []
        self.visited_States_Number = 0
        self.visited = set()
        self.Draw = Draw_Board_Pygame()
    
    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        return memory_mb
    
    def Print_Path_Goal(self , current_state) :
        State_From_Goal_Path = deepcopy(current_state)
        while(State_From_Goal_Path.Parent != None) :
            self.Path_Goal_List.append(State_From_Goal_Path)
            State_From_Goal_Path = State_From_Goal_Path.Parent

        self.Path_Goal_List.append(State_From_Goal_Path)
        self.Path_Goal_List.reverse()
        print("all States That Generated Path are:")
        print('\n')
        for state in self.Path_Goal_List :
            print (state)

        print("the Number States From Init State To Goal State are :")
        Length = len(self.Path_Goal_List)
        print (Length)
        print("the Number States That Visited are :")           
        print (self.visited_States_Number)
    
    def Get_Time_and_Meomory(self , start_time , initial_memory) :
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Time taken by the algorithm : {execution_time:.2f} ")
        final_memory = self.get_memory_usage()
        memory_used = final_memory - initial_memory
        print(f"Memory Used: {memory_used:.2f} MB")
        print(f"Total Memory Usage: {final_memory:.2f} MB")

    def Depth_First_Search_BY_Recursion(self , current_state) :  
        start_time = time.time()
        initial_memory = self.get_memory_usage()
        if current_state in self.visited:
            return False       
        self.visited.add(current_state)   
        if current_state.isGoal() :
            self.visited.add(current_state)
            print(current_state)
            self.Draw.draw_Screen_Game(current_state.board)
            print("Gaaaaaaaaaame Oveeeeeeeeeeeer")
            self.Print_Path_Goal(current_state)
            self.Get_Time_and_Meomory(start_time , initial_memory)
            return True       
        print(current_state)
        self.Draw.draw_Screen_Game(current_state.board)  
        Next_States = current_state.Get_Next_States()           
        for state in Next_States :               
            if state.isLoss() :
                continue
            if state not in self.visited :
                state.Parent = current_state
                self.visited_States_Number += 1 
                result = self.Depth_First_Search_BY_Recursion(state)
                if result:  
                    return True        
        return False
        

#********************************************************************************************#


# file name : Unifrom_Cost_Search.py ********************************************************************
# for solve the game using UCS
from copy import deepcopy
import heapq
from Draw_Board_Pygame import Draw_Board_Pygame
import psutil
import time 
import os 

class Unifrom_Cost_Search:
    def __init__(self , init_state) -> None:
        self.init_state = init_state
        self.current_state = deepcopy(init_state)
        self.current_state.cost = 0
        self.Path_Goal_List = []
        self.visited_States_Number = 0
        self.priority_queue = [] 
        heapq.heappush(self.priority_queue, self.current_state)
        self.visited = set()  
        self.visited.add(init_state)  
        self.Draw = Draw_Board_Pygame()
    
    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        return memory_mb

    def Print_Path_Goal(self , current_state) :
            State_From_Goal_Path = deepcopy(current_state)
            while(State_From_Goal_Path.Parent != None) :
                self.Path_Goal_List.append(State_From_Goal_Path)
                State_From_Goal_Path = State_From_Goal_Path.Parent

            self.Path_Goal_List.append(State_From_Goal_Path)
            self.Path_Goal_List.reverse()
            print("all States That Generated Path are:")
            print('\n')
            for state in self.Path_Goal_List :
                print (state)
                

            print("the Number States From Init State To Goal State are :")
            Length = len(self.Path_Goal_List)
            print (Length)
            print("the Number States That Visited are :")           
            print (self.visited_States_Number)
            
    def Get_Time_and_Meomory(self , start_time , initial_memory) :
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Time taken by the algorithm : {execution_time:.2f} ")
        final_memory = self.get_memory_usage()
        memory_used = final_memory - initial_memory
        print(f"Memory Used: {memory_used:.2f} MB")
        print(f"Total Memory Usage: {final_memory:.2f} MB") 

    def Unifrom_Cost_Search_Solve(self) :
        start_time = time.time()
        initial_memory = self.get_memory_usage()
        while self.priority_queue :
            self.current_state = heapq.heappop(self.priority_queue)
            if self.current_state.isGoal() :
                self.visited.add(self.current_state) 
                print(self.current_state)
                self.Draw.draw_Screen_Game(self.current_state.board)
                print("Gaaaaaaaaaame Oveeeeeeeeeeeer")
                self.Print_Path_Goal(self.current_state)
                self.Get_Time_and_Meomory(start_time , initial_memory)
                return None 
            print(self.current_state)
            self.Draw.draw_Screen_Game(self.current_state.board)     
            Next_States = self.current_state.Get_Next_States()  
            if (not Next_States) :
                continue        
            for state in Next_States :               
                if state.isLoss() :
                    continue
                if state not in self.visited :
                    total_cost = self.current_state.cost + state.cost
                    state.cost = total_cost               
                    self.visited_States_Number += 1     
                    self.visited.add(state)   
                    state.Parent = self.current_state                
                    heapq.heappush(self.priority_queue, state)                    
        return None
       
            
#********************************************************************************************#


# file name : User_Play.py ********************************************************************
# This file allows the player to play the game himself
from copy import deepcopy
from Draw_Board_Pygame import Draw_Board_Pygame
from Directions import Directions
import pygame
import sys


class User_Play:
    def __init__(self , init_state) -> None:
        self.init_state = init_state
        self.current_state = init_state.copy()
        self.states = []
        self.states.append(init_state)
        self.Draw = Draw_Board_Pygame()
        
    def Get_All_States(self):
        for state in self.states:
            print (state)

    def Play_Game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.Move_By_User_Direction("UP")
                    elif event.key == pygame.K_DOWN:
                        self.Move_By_User_Direction("DOWN")
                    elif event.key == pygame.K_LEFT:
                        self.Move_By_User_Direction("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.Move_By_User_Direction("RIGHT")                    
                    print(self.current_state)
                    self.states.append(deepcopy(self.current_state))
            if self.current_state.isGoal():
                print('Gaaaaaaaaaaaaaame Oveeeeeeeeeeeeer')
                self.Get_All_States()
                running = False
            if self.current_state.isLoss():
                print('yooooooooooooooou Loooooooooooooos')
                self.Get_All_States()
                running = False
            self.Draw.draw_Screen_Game(self.current_state.board)

    def Move_By_User_Direction(self, direction):
        directions = Directions().Return_Directions()
        dx, dy = directions[direction]
        Players_can_move = [
            player for player in self.current_state.Players_List 
            if self.current_state.checkMove(dx, dy, player)
            ]
        if direction in ['DOWN', 'RIGHT']:
            Players_can_move.reverse()
        for square in Players_can_move:
            x, y = 0, 0
            while True:
                x += dx
                y += dy   
                if not self.current_state.checkMove(x, y, square):
                    break    
                if self.current_state.player_Reach_Target(x, y, square):
                    x, y = x + dx, y + dy
                    break   
                if self.current_state.player_Reach_To_Loss_Square(x, y, square):
                    break 
                if self.current_state.player_Reach_To_Variable_Square(x, y, square):
                    self.current_state.change_Variable_Square_To_Goal_Square(square.x + x, square.y + y, square.target_square)                    
            if direction == 'UP':
                new_x, new_y = square.x + x - dx, square.y + y
            elif direction == 'DOWN':
                new_x, new_y = square.x + x - dx, square.y + y
            elif direction == 'LEFT':
                new_x, new_y = square.x + x, square.y + y - dy
            else:   
                new_x, new_y = square.x + x , square.y + y - dy
            square.new_x, square.new_y = new_x, new_y
            self.current_state.change_Player_Move(square) 
  

#********************************************************************************************#


# file name : Draw_Board_Pygame.py ********************************************************************
# This file is for drawing the interface related to solving the game , 
# whether the user is playing or the search algorithm is solving it 
import pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (244, 67, 54 , 1)
ORANGE = (255, 0, 104 , 1)
BLUE = (18, 144, 227 , 1)
YELLOW = (255, 238, 0 , 1)
GREEN = (0, 255, 97 , 1)
GRAY = (192 , 192 , 192)
DARK_BLUE = (2 , 32 , 59 , 1)
SCREEN_COLOR = (220, 240, 240)
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700
TILE_SIZE = 40 
LIGHT_BLUE = (18, 144, 227)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zero Squares Game")
font = pygame.font.Font(None, 40)


class Draw_Board_Pygame :

    def draw_board(self , init_board):
        board_width = len(init_board[0]) * TILE_SIZE
        board_height = len(init_board) * TILE_SIZE
        start_x = (WINDOW_WIDTH - board_width) // 2
        start_y = (WINDOW_HEIGHT - board_height) // 2
        for row_index, row in enumerate(init_board):
            for col_index, tile in enumerate(row):
                x = start_x + col_index * TILE_SIZE
                y = start_y + row_index * TILE_SIZE
                if tile.type == 'Black':
                    pygame.draw.rect(screen, DARK_BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile.type == 'Red':
                    pygame.draw.rect(screen, RED, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile.type == 'Orange':
                    pygame.draw.rect(screen, ORANGE, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile.type == 'Blue':
                    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile.type == 'Yellow':
                    pygame.draw.rect(screen, YELLOW, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile.type == 'Green':
                    pygame.draw.rect(screen, GREEN, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile.type == 'RedGoal':
                    pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, RED, (x, y, TILE_SIZE, TILE_SIZE),4)  
                elif tile.type == 'OrangeGoal':
                    pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, ORANGE, (x, y, TILE_SIZE, TILE_SIZE),4)  
                elif tile.type == 'BlueGoal':
                    pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE),4)  
                elif tile.type == 'YellowGoal':
                    pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, YELLOW, (x, y, TILE_SIZE, TILE_SIZE),4)  
                elif tile.type == 'GreenGoal':
                    pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, GREEN, (x, y, TILE_SIZE, TILE_SIZE),4) 
                elif tile.type == 'BlackWhite':
                    pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE),4) 
                elif tile.type == 'WhiteWhite':
                    pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE),4) 

    def draw_Screen_Game(self , init_State):
        screen.fill(SCREEN_COLOR)
        self.draw_board(init_State)
        pygame.display.flip()
     

#********************************************************************************************#


# file name : Level_Selection_Menu.py ********************************************************************
# Interface that allows the user to select the game level(board Array)
import pygame
import sys

WHITE = (255, 255, 255)
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700
TILE_SIZE = 40 
RE_START_BUTTON = (171, 141, 239 ,1)
DARK_BLUE_BUTTON = (2, 32, 59)
LIGHT_BLUE = (18, 144, 227)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zero Squares Game")
font = pygame.font.Font(None, 40)

class Level_Selection_Menu :
     
    def __init__(self):
        self.scroll_offset = 0

    def draw_button(self , screen, text , pos, color , hover_color , font):
        text_surface = font.render(text, True, WHITE)
        button_rect = text_surface.get_rect(center=pos)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, button_rect.inflate(20, 10))
        else:
            pygame.draw.rect(screen, color, button_rect.inflate(20, 10))
        screen.blit(text_surface, button_rect)
        return button_rect
    
    def level_selection_menu(self):
        button_height = 60
        total_buttons = 30
        button_spacing = 20
        running = True
        while running:
            screen.fill((220, 240, 240))
            # Scrollable area
            scroll_area_height = total_buttons * (button_height + button_spacing)
            start_y = self.scroll_offset
            # Draw buttons
            buttons = []
            for i in range(total_buttons):
                button_y = start_y + i * (button_height + button_spacing)
                button_pos = (WINDOW_WIDTH // 2, button_y + button_height // 2)
                button_rect = self.draw_button(screen, f"Level {i + 1}", button_pos, DARK_BLUE_BUTTON, LIGHT_BLUE, font)
                buttons.append(button_rect)
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        for i, rect in enumerate(buttons):
                            if rect.collidepoint(event.pos):
                                print(f"Level {i + 1} selected!")
                                # pygame.quit()
                                return i + 1
                elif event.type == pygame.MOUSEWHEEL:
                    # Scroll logic
                    self.scroll_offset += event.y * 20  # Adjust scroll speed
                    self.scroll_offset = max(min(self.scroll_offset, 0), -(scroll_area_height - WINDOW_HEIGHT))

            pygame.display.flip()
            # clock.tick(30)


#********************************************************************************************#


# file name : Main_Menu_GUI.py ********************************************************************
# To build the main GUI
from Zero_Squares_Game import Zero_Squares_Game
from Options_Menu_GUI import Options_Menu_GUI
import pygame
import sys

WHITE = (255, 255, 255)
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700
TILE_SIZE = 40 
RE_START_BUTTON = (171, 141, 239 ,1)
DARK_BLUE_BUTTON = (2, 32, 59)
LIGHT_BLUE = (18, 144, 227)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zero Squares Game")
font = pygame.font.Font(None, 40)

class Main_Menu_GUI :
    
    def draw_button(self , screen, text , pos, color , hover_color , font):
        text_surface = font.render(text, True, WHITE)
        button_rect = text_surface.get_rect(center=pos)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, button_rect.inflate(20, 10))
        else:
            pygame.draw.rect(screen, color, button_rect.inflate(20, 10))
        screen.blit(text_surface, button_rect)
        return button_rect

    def main_menu(self , init_State):
        while True:
            screen.fill((220, 240, 240))
            options_button = self.draw_button(screen, "Options", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            start_button = self.draw_button(screen, "Start Game", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            quit_button = self.draw_button(screen, "Exit", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        game = Zero_Squares_Game(init_State)
                        game.User_Play()
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif options_button.collidepoint(event.pos):
                        Options_Menu_GUI().Options_menu(init_State)

            pygame.display.flip()
            # clock.tick(30)


#********************************************************************************************#


# file name : Options_Menu_GUI.py ********************************************************************
# This interface allows the user to choose which search algorithm to apply to solve the game
from Zero_Squares_Game import Zero_Squares_Game
from Zero_Squares_LeveLs import Zero_Squares_LeveLs
from Level_Selection_Menu import Level_Selection_Menu
import pygame
import sys

WHITE = (255, 255, 255)
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700
DARK_BLUE_BUTTON = (2, 32, 59)
LIGHT_BLUE = (18, 144, 227)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zero Squares Game")
font = pygame.font.Font(None, 40)

class Options_Menu_GUI :

    def draw_button(self , screen, text , pos, color , hover_color , font):
        text_surface = font.render(text, True, WHITE)
        button_rect = text_surface.get_rect(center=pos)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, button_rect.inflate(20, 10))
        else:
            pygame.draw.rect(screen, color, button_rect.inflate(20, 10))
        screen.blit(text_surface, button_rect)
        return button_rect
    
    def Options_menu(self , init_State):
        from Main_Menu_GUI import Main_Menu_GUI  # Lazy import
        while True:
            screen.fill((220, 240, 240)) 
            User_PLay_button = self.draw_button(screen, "User PLay", (WINDOW_WIDTH // 2  , WINDOW_HEIGHT // 2 - 250), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            DFS_button = self.draw_button(screen, "Depth_First_Search", (WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT // 2 - 150), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            DFS_R_button = self.draw_button(screen, "Depth_First_Search_Recursion",(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 180), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            BFS_button = self.draw_button(screen, "Breadth_First_Search", (WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT // 2 - 50), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            UCS_button = self.draw_button(screen, "Uniform_Cost_Search", (WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT // 2 + 50), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            HCS_button = self.draw_button(screen, "Hill_Climbing_Search", (WINDOW_WIDTH // 2 + 300, WINDOW_HEIGHT // 2 - 150), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            AStar_button = self.draw_button(screen, "A* Search Algorithm", (WINDOW_WIDTH // 2 + 300, WINDOW_HEIGHT // 2 - 50), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            Select_Level = self.draw_button(screen, "Select_Level", (WINDOW_WIDTH // 2 + 300, WINDOW_HEIGHT // 2 + 50), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            Go_Back_button  = self.draw_button(screen, "Go Back Menu", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 290), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if User_PLay_button.collidepoint(event.pos):
                        game = Zero_Squares_Game(init_State)
                        game.User_Play()
                    elif DFS_button.collidepoint(event.pos):
                        game = Zero_Squares_Game(init_State)
                        game.Depth_First_Search()
                    elif DFS_R_button.collidepoint(event.pos):
                        game = Zero_Squares_Game(init_State)
                        game.Depth_First_Search_Recursion()
                    elif BFS_button.collidepoint(event.pos):
                        game = Zero_Squares_Game(init_State)
                        game.Breadth_First_Search()
                    elif UCS_button.collidepoint(event.pos):
                        game = Zero_Squares_Game(init_State)
                        game.Unifrom_Cost_Search()
                    elif HCS_button.collidepoint(event.pos):
                        game = Zero_Squares_Game(init_State)
                        game.Hill_Climbing_Search()
                    elif Select_Level.collidepoint(event.pos):
                        Level_Object = Level_Selection_Menu()
                        Level_Selected = Level_Object.level_selection_menu() - 1
                        init_state = Zero_Squares_LeveLs(Level_Selected).Return_Array_Object()
                        Main_Menu_GUI().main_menu(init_state)                  
                    elif Go_Back_button.collidepoint(event.pos):
                        Main_Menu_GUI().main_menu(init_State)                  
            pygame.display.flip()


#********************************************************************************************#


# file name : Zero_Squares_Game.py ********************************************************************
# The function of this file is to run the search algorithm that was selected from the optios interface
from User_Play import User_Play
from Depth_First_Search import Depth_First_Search
from Breadth_First_Search import Breadth_First_Search
from DFS_By_Recursion import DFS_By_Recursion
from Uniform_Cost_Search import Unifrom_Cost_Search


class Zero_Squares_Game:

    def __init__(self , init_state) -> None:
        self.init_state = init_state

    def User_Play(self):
       game = User_Play(self.init_state)
       game.Play_Game()

    def Depth_First_Search(self) :
        game = Depth_First_Search(self.init_state)
        game.Depth_First_Search_Solve()

    def Depth_First_Search_Recursion(self) :
        game = DFS_By_Recursion()
        game.Depth_First_Search_BY_Recursion(self.init_state)

    def Breadth_First_Search(self) :
        game = Breadth_First_Search(self.init_state)
        game.Breadth_First_Search_Solve()

    def Unifrom_Cost_Search(self) :
        game = Unifrom_Cost_Search(self.init_state)
        game.Unifrom_Cost_Search_Solve()


#********************************************************************************************#