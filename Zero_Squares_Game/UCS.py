from copy import deepcopy
import heapq
from Draw_Board_Pygame import Draw_Board_Pygame
import os 


class UCS :  
    def __init__(self , init_state) -> None:
        self.init_state = init_state
        self.current_state = deepcopy(init_state)
        self.current_state.cost = 0
        self.Path_Goal_List = []
        self.visited_States_Number = 0
        self.priority_queue = [] 
        heapq.heappush(self.priority_queue, self.current_state)
         
        self.visited = []
        self.visited.append(init_state)
        self.Draw = Draw_Board_Pygame()

    def UCS(self) :
        while self.priority_queue :
            self.current_state = heapq.heappop(self.priority_queue)
            if self.current_state.isGoal() :
                self.visited.append(deepcopy(self.current_state))
                print(self.current_state)
                self.Draw.draw_Screen_Game(self.current_state.board)

                State_From_Goal_Path = deepcopy(self.current_state)
                while(State_From_Goal_Path.Parent != None) :
                    self.Path_Goal_List.append(State_From_Goal_Path)
                    State_From_Goal_Path = State_From_Goal_Path.Parent

                self.Path_Goal_List.append(State_From_Goal_Path)
                self.Path_Goal_List.reverse()
                print(" Path :")
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

                return None
            
            print(self.current_state)
            self.Draw.draw_Screen_Game(self.current_state.board)  

            visited = False
            for vis in self.visited :
                if self.current_state == vis :
                    visited = True
                    break
            if visited == False:
                self.visited.append(self.current_state)
            

            Next_States = self.current_state.Get_Next_States()           
            for state in Next_States :
                if state.isLoss() :
                    continue
                visited = False
                for vis in self.visited :                                              
                    if state == vis :
                        visited = True
                        break               
                if visited == False:
                    total_cost = self.current_state.cost + state.cost
                    state.cost = total_cost               
                    self.visited_States_Number += 1    
                    state.Parent = self.current_state
                    heapq.heappush(self.priority_queue, state)
        return None
       
            