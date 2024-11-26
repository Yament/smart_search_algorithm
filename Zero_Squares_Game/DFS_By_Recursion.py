
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

    def Depth_First_Search_BY_Recursion(self , current_state) :    
        self.visited.add(deepcopy(current_state))  
        if current_state.isGoal() :
            self.visited.add(deepcopy(current_state))
            print(current_state)
            self.Draw.draw_Screen_Game(current_state.board)
            print("Gaaaaaaaaaame Oveeeeeeeeeeeer")

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

            print('\n')
            print('\n')
            print("the Number States From Init State To Goal State are :")
            Length = len(self.Path_Goal_List)
            print (Length)
            print("the Number States That Visited are :")           
            print (self.visited_States_Number)

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
        







        