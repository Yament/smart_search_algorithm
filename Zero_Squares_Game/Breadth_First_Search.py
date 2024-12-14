
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
            self.visited_States_Number += 1 
            if self.current_state.isGoal() :
                self.visited.add(self.current_state)
                # print(self.current_state)
                self.Draw.draw_Screen_Game(self.current_state.board)
                print("Gaaaaaaaaaame Oveeeeeeeeeeeer")
                self.Print_Path_Goal(self.current_state)
                self.Get_Time_and_Meomory(start_time , initial_memory)
                return None        
            # print(self.current_state)
            self.Draw.draw_Screen_Game(self.current_state.board) 
            Next_States = self.current_state.Get_Next_States()           
            for state in Next_States :               
                if state.isLoss() :
                    continue
                if state not in self.visited :
                    state.Parent = self.current_state
                    self.visited.add(state)
                    self.queue.append(state)     
        return None
        



         

