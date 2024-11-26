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

                State_From_Goal_Path = deepcopy(self.current_state)
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


                end_time = time.time()
                execution_time = end_time - start_time
                print("Time taken by the algorithm : ")
                print (execution_time)

                final_memory = self.get_memory_usage()
                memory_used = final_memory - initial_memory
                print(f"Memory Used: {memory_used:.2f} MB")
                print(f"Total Memory Usage: {final_memory:.2f} MB")

                return None
            
            print(self.current_state)
            self.Draw.draw_Screen_Game(self.current_state.board)  
            
            Next_States = self.current_state.Get_Next_States()           
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
       
            