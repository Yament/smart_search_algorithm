
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
  
 







 

















