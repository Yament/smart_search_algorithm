from copy import deepcopy
import pygame
import sys

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
 
RE_START_BUTTON = (171, 141, 239 ,1)
DARK_BLUE_BUTTON = (2, 32, 59)
LIGHT_BLUE = (18, 144, 227)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zero Squares Game")
font = pygame.font.Font(None, 40)
Directions = ['LEFT' , 'RIGHT' , 'DOWN' , 'UP']
 
class Square:

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
           return '🔲🟥' 
        elif self.type == 'OrangeGoal':
           return '🔲🟧'
        elif self.type == 'BlueGoal':
           return '🔲🟦'
        elif self.type == 'YellowGoal':
           return '🔲🟨' 
        elif self.type == 'GreenGoal':
           return '🔲🟩'        
        elif self.type == 'BlackWhite':
           return '🔲⬛' 
        elif self.type == 'WhiteWhite':
           return '🔲⬜' 


    def __eq__(self, other):
        if not isinstance(other, Square):
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
        
class State:

    def __init__(self,rows,cols,board)-> None:
        self.rows = rows
        self.cols = cols
        self.board = board
        self.Players_List  = self.Get_All_Players()
        self.direction = None
    
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
        Next_States = []
        for direction in Directions :
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
                
class Zero_Squares_Game:

    def __init__(self , init_state) -> None:
        self.init_state = init_state
        self.current_state = deepcopy(init_state)
        self.states = []
        self.states.append(init_state)

    def Get_All_States(self):
        for state in self.states:
            print (state)

    def User_Play(self):
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
            draw_Screen_Game(self.current_state.board)
 
    def Move_By_User_Direction(self , direction):

        ########################################################## MOVE UP
        if direction == 'UP':
            Players_can_move = []
            for player in self.current_state.Players_List :
                if(self.current_state.checkMove(-1 , 0 , player)):
                    Players_can_move.append(player)
                else :
                    continue     
            for square in Players_can_move:                                             
                x , y = 0 , 0
                while (True) :
                    x = x - 1 
                    if not self.current_state.checkMove(x , y , square) :
                        break
                    if self.current_state.playerReachTarget(x , y , square) :
                        x = x - 1
                        break
                    if self.current_state.player_Reach_To_Loss_Square(x , y , square) :
                        x = x - 1
                        break
                    if self.current_state.player_Reach_To_Variable_Square(x , y , square) :
                        self.current_state.change_Variable_Square_To_Goal_Square(square.x + x , square.y + y , square.target_square)         
                new_player_x , new_player_y = square.x + x + 1 , square.y + y
                square.new_x , square.new_y = new_player_x , new_player_y
                self.current_state.change_Player_Move(square)                  

        ########################################################## MOVE DOWN
        elif direction == 'DOWN':
            Players_can_move = []
            for player in self.current_state.Players_List :
                if(self.current_state.checkMove(1 , 0 , player)):
                    Players_can_move.append(player)
                else :
                    continue 
            Players_can_move.reverse()    
            for square in Players_can_move:                                                     
                x , y = 0 , 0
                while (True) :
                    x = x + 1
                    if not self.current_state.checkMove(x , y , square) :
                        break
                    if self.current_state.playerReachTarget(x , y , square) :
                        x = x + 1
                        break 
                    if self.current_state.player_Reach_To_Loss_Square(x , y , square) :
                        x = x + 1
                        break
                    if self.current_state.player_Reach_To_Variable_Square(x , y , square) :                       
                        self.current_state.change_Variable_Square_To_Goal_Square(square.x + x , square.y + y , square.target_square) 
                new_player_x , new_player_y = square.x + x - 1 , square.y + y
                square.new_x , square.new_y = new_player_x , new_player_y
                self.current_state.change_Player_Move(square)                                      
        
        ########################################################## MOVE LEFT
        elif direction == 'LEFT':
            Players_can_move = []
            for player in self.current_state.Players_List :
                if(self.current_state.checkMove(0 , -1 , player)):
                    Players_can_move.append(player)
                else :
                    continue     
            for square in Players_can_move:                
                x , y = 0 , 0
                while (True) :
                    y = y - 1
                    if not self.current_state.checkMove(x , y , square) :
                        break
                    if self.current_state.playerReachTarget(x , y , square) :
                        y = y - 1
                        break
                    if self.current_state.player_Reach_To_Loss_Square(x , y , square) :
                        y = y - 1
                        break
                    if self.current_state.player_Reach_To_Variable_Square(x , y , square) :
                        self.current_state.change_Variable_Square_To_Goal_Square(square.x + x , square.y + y , square.target_square) 
                new_player_x , new_player_y = square.x + x , square.y + y + 1
                square.new_x , square.new_y = new_player_x , new_player_y
                self.current_state.change_Player_Move(square) 

        ########################################################## MOVE RIGHT
        elif direction == 'RIGHT':
            Players_can_move = []
            for player in self.current_state.Players_List :
                if(self.current_state.checkMove(0 , 1 , player)):
                    Players_can_move.append(player)
                else :
                    continue               
            Players_can_move.reverse()
            for square in Players_can_move:              
                x , y = 0 , 0
                while (True) :
                    y = y + 1
                    if not self.current_state.checkMove(x , y , square) :
                        break
                    if self.current_state.playerReachTarget(x , y , square) :
                        y = y + 1
                        break
                    if self.current_state.player_Reach_To_Loss_Square(x , y , square) :
                        y = y + 1
                        break
                    if self.current_state.player_Reach_To_Variable_Square(x , y , square) :
                        self.current_state.change_Variable_Square_To_Goal_Square(square.x + x , square.y + y , square.target_square) 
                new_player_x , new_player_y = square.x + x , square.y + y - 1
                square.new_x , square.new_y = new_player_x , new_player_y
                self.current_state.change_Player_Move(square) 
      
    
        

 
    
def draw_board(screen , init_board):
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

def draw_Screen_Game(init_State):
    screen.fill(SCREEN_COLOR)
    draw_board(screen , init_State)
    restart_button = draw_button(screen, "Re_Start", (WINDOW_WIDTH // 2 + 400, WINDOW_HEIGHT // 2 + 300), GREEN, LIGHT_BLUE, font)
    pygame.display.flip()
 
def draw_button(screen, text, pos, color, hover_color, font):
    text_surface = font.render(text, True, WHITE)
    button_rect = text_surface.get_rect(center=pos)
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect.inflate(20, 10))
    else:
        pygame.draw.rect(screen, color, button_rect.inflate(20, 10))
    screen.blit(text_surface, button_rect)
    return button_rect

def main_menu(init_State):
    while True:
        screen.fill((220, 240, 240))
        options_button = draw_button(screen, "Options", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
        start_button = draw_button(screen, "Start Game", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
        quit_button = draw_button(screen, "Exit", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
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
                    Options_menu(init_State)

        pygame.display.flip()
        clock.tick(30)
 
def Options_menu(init_State):
    while True:
        screen.fill((220, 240, 240)) 
        User_PLay_button = draw_button(screen, "User PLay", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 300), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
        DFS_button = draw_button(screen, "Depth_First_Search", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 200), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
        BFS_button = draw_button(screen, "Breadth_First_Search", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
        UCS_button = draw_button(screen, "Uniform_Cost_Search", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 0), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
        HCS_button = draw_button(screen, "Hill_Climbing_Search", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
        AStar_button = draw_button(screen, "A* Search Algorithm", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
        Go_Back_button  = draw_button(screen, "Go Back Menu", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 300), DARK_BLUE_BUTTON, LIGHT_BLUE, font)
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
                    # game.Depth_First_Search()
                elif Go_Back_button.collidepoint(event.pos):
                    main_menu(init_State)
                

        pygame.display.flip()
        clock.tick(30)

def main():

    #Array size  8 x 12
    # init_board =[
    # ['⬜' , '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬜' , '⬜', '⬛', '🟥', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '🔲🟥', '⬜', '⬜', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬜' , '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]


    # 9 x 11
    # init_board =[
    # ['⬜' , '⬜', '⬜', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜'],

    # ['⬜' , '⬜', '⬜', '⬛', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬛', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '🔲🟥', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '🟥', '⬜', '⬜', '⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜'],
    # ]

    # 9 x 10
    # init_board =[
    # ['⬜' , '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜'],

    # ['⬜' , '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬜'],

    # ['⬜' , '⬛', '⬛', '⬜', '⬜', '🔲🟥', '⬜', '⬜', '⬛', '⬜'],

    # ['⬛' , '⬛', '⬜', '⬜', '⬜', '⬜', '⬛', '🟥', '⬛', '⬜'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜'],

    # ]

    # 6 x 8
    # init_board =[
    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '🟥', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '🔲🟥', '⬛', '⬛', '⬛'],

    # ['⬜' , '⬜', '⬜', '⬛', '⬛', '⬛', '⬜', '⬜'],
    # ]


    # 3 x 8
    # init_board =[
    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '🟥', '⬜', '⬜', '⬜', '⬜', '🔲🟥', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]

    # 5 x 9
    # init_board =[
    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜'],

    # ['⬛' , '🔲🟥', '⬜', '⬜', '⬜', '⬛', '⬛', '⬜', '⬜'],

    # ['⬛' , '⬜', '⬜', '🔲🟦', '⬜', '⬜', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '🟦', '🟥', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]


    # 8 x 9
    # init_board =[
    # ['⬜' , '⬜', '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬜' , '⬜', '⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '🔲🟥', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '🟥', '⬜', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '🔲🟦', '⬛', '🟦', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]

    # 11 x 7
    # init_board =[
    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛' , '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '🔲🟦' , '⬛'],

    # ['⬛' , '⬜', '⬜', '🟦', '⬛', '⬜' , '⬛'],

    # ['⬛' , '🟥', '⬛', '⬜', '⬛', '⬜' , '⬛'],

    # ['⬛' , '⬜', '⬜', '🔲🟥', '⬛', '⬜' , '⬛'],

    # ['⬛' , '⬜', '⬜', '⬛', '⬛', '⬜' , '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜' , '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬛' , '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬜', '⬜' , '⬛'],

    # ['⬜' , '⬛', '⬜', '⬜', '⬜', '⬜' , '⬛'],

    # ['⬜' , '⬛', '⬛', '⬛', '⬛', '⬛' , '⬛'],
    # ]


    # 8 x 11
    # init_board =[
    # ['⬜' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜'],

    # ['⬛' , '⬛', '🟥', '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬛', '⬛', '🔲🟦', '⬜', '⬛', '⬜'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬛', '⬛', '⬛', '⬜', '⬜', '🔲🟥', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬛'],

    # ['⬛' , '⬛', '🟦', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜'],

    # ['⬜' , '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
    # ]


    # 8 x 12
    # init_board =[
    # ['⬜' , '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜'],

    # ['⬜' , '⬛', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬛', '⬜'],

    # ['⬛' , '⬛', '⬜', '⬜', '⬛', '⬜', '🔲🟦', '⬛', '⬜', '⬜', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬛', '⬜', '🔲🟥', '⬜', '⬜', '⬛', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬛', '⬜', '⬜', '⬛', '⬛', '⬜', '⬛'],

    # ['⬛' , '🟥', '⬛', '⬜', '⬛', '⬛', '⬜', '⬜', '⬜', '⬛', '🟦', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]


    # 5 x 8
    # init_board =[
    # ['⬜' , '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '⬜'],

    # ['⬛' , '⬛', '🔲🟧', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '🟧', '🟥', '🟦', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '🔲🟦', '⬛', '🔲🟥', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜'],
    # ]

    # 8 x 7
    # init_board =[
    # ['⬜' , '⬜', '⬛', '⬛', '⬛', '⬛' , '⬛'],

    # ['⬛' , '⬛', '⬛', '⬜', '🔲🟧', '⬜' , '⬛'],

    # ['⬛' , '🔲🟥', '⬜', '⬜', '⬜', '⬜' , '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬛', '🟥' , '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬛', '🟧' , '⬛'],

    # ['⬛' , '⬛', '🔲🟦', '⬜', '⬛', '🟦' , '⬛'],

    # ['⬜' , '⬛', '⬛', '⬜', '⬛', '⬛' , '⬛'],

    # ['⬜' , '⬜', '⬛', '⬛', '⬛', '⬜' , '⬜'],
    # ]

    # 8 x 11
    # init_board =[
    # ['⬜' , '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '⬜'],

    # ['⬛' , '⬛', '⬛', '🟦', '🟥', '🟧', '⬛', '⬜', '⬜', '⬜', '⬜'],

    # ['⬛' , '⬜', '⬛', '⬜', '⬜', '🔲🟦', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬛', '🔲🟥', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬛', '⬛', '⬜', '⬛', '⬛', '⬛', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬛', '🔲🟧', '⬜', '⬜', '⬜', '⬛', '⬛', '⬜'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜'],
    # ]

    # 7 x 7
    # init_board =[
    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛' , '⬛'],

    # ['⬛' , '🔲🟦', '⬛', '🔲🟧', '⬛', '🔲🟥' , '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜' , '⬛'],

    # ['⬛' , '🟧', '⬜', '⬜', '⬜', '⬜' , '⬛'],

    # ['⬛' , '⬛', '⬜', '⬜', '⬜', '⬜' , '⬛'],

    # ['⬜' , '⬛', '⬜', '🟥', '⬜', '🟦' , '⬛'],

    # ['⬜' , '⬛', '⬛', '⬛', '⬛', '⬛' , '⬛'],
    # ]

    # 9 x 8
    # init_board =[
    # ['⬜' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬜' , '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬜' , '⬛', '⬜', '🔲🟦', '⬜', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬜', '⬛', '⬛', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '🟧', '🟥', '🟦', '⬜', '⬜', '⬛'],
    
    # ['⬛' , '⬜', '⬛', '⬛', '⬛', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬛', '⬜', '🔲🟧', '⬛', '🔲🟥', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]
 
    # 7 x 11
#     init_board =[
#     ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],

#     ['⬛' , '🟧', '🟥', '🟦', '🟩', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

#   ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '🔲🟧', '⬜', '⬜', '⬜', '⬛'],

#     ['⬛' , '⬛', '⬜', '⬜', '⬜', '🔲🟩', '⬜', '⬜', '⬜', '⬜', '⬛'],

#     ['⬜' , '⬛', '⬜', '⬜', '🔲🟦', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛'],

#     ['⬜' , '⬛', '⬜', '🔲🟥', '⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬜'],

#     ['⬜' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '⬜'],
#     ]

 # 11 x 9
    # init_board =[
    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛' , '⬛', '⬜' , '⬜'],

    # ['⬛' , '🟥', '⬜', '⬜', '⬜', '🟦' , '⬛', '⬛' , '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜' , '⬛', '🔲🟧' , '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬜', '⬜' , '⬛', '⬜' , '⬛'],

    # ['⬜' , '⬜', '⬛', '⬜', '⬜', '⬜' , '⬜', '⬜' , '⬛'],

    # ['⬛' , '⬛', '⬛', '⬜', '⬛', '⬛' , '⬜', '⬜' , '⬛'],

    # ['⬛' , '🟩', '⬜', '🔲🟩', '⬛', '🔲🟥' , '⬜', '⬜' , '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜' , '⬜', '⬜' , '⬛'],

    # ['⬛' , '🟧', '⬜', '⬜', '⬜', '⬜' , '⬜', '⬜' , '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛' , '⬛', '🔲🟦' , '⬛'],

    # ['⬜' , '⬜', '⬜', '⬜', '⬜', '⬜' , '⬛', '⬛' , '⬛'],
    # ]
 

 # 12 x 8  **********************************************************
    # init_board =[
    # ['⬜' , '⬛', '⬛', '⬛', '⬜', '⬜' , '⬜' , '⬜'],

    # ['⬛' , '⬛', '🔲🟧', '⬛', '⬛', '⬜' , '⬜' , '⬜'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬛', '⬜' , '⬜' , '⬜'],

    # ['⬛' , '⬛', '⬛', '⬜', '⬛', '⬛' , '⬛' , '⬛'],

    # ['⬛' , '🟦', '⬜', '⬜', '🟧', '⬛' , '⬛' , '⬛'],

    # ['⬛' , '⬛', '⬜', '⬜', '⬜', '⬜' , '⬜' , '⬛'],

    # ['⬛' , '🟥', '⬜', '⬛', '🔲🟥', '⬜' , '🟩' , '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬜', '⬛' , '⬛' , '⬛'],

    # ['⬜' , '⬜', '⬜', '⬛', '⬜', '🔲🟦' , '⬜' , '⬛'],

    # ['⬜' , '⬜', '⬜', '⬛', '⬜', '⬜' , '⬜' , '⬛'],

    # ['⬜' , '⬜', '⬜', '⬛', '⬛', '🔲🟩' , '⬛' , '⬛'],

    # ['⬜' , '⬜', '⬜', '⬜', '⬛', '⬛' , '⬛' , '⬜'],
    # ]
 
    # 6 x 9
    # init_board =[
    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '🟥', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '🔲⬛'],

    # ['⬛' , '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '🔲🟥', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]

 
    # 6 x 8
    # init_board =[
    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬛'],

    # ['🔲⬛' , '⬜', '⬜', '🟦', '🟥', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '🔲🟦', '⬜', '⬜', '⬜', '⬛', '⬛'],

    # ['⬛' , '🔲🟥', '⬜', '⬜', '⬜', '⬜', '⬛', '⬜'],

    # ['⬛' , '⬛', '⬛', '🔲⬛', '⬛', '⬛', '⬛', '⬜'],
    # ]



    # 7 x 7
    # init_board =[
    # ['⬜' , '⬜', '🔲⬛', '⬛', '⬛', '⬛' , '⬛'],

    # ['⬜' , '🔲⬛', '⬜', '🔲🟦', '⬜', '⬜' , '⬛'],

    # ['🔲⬛' , '🔲🟥', '⬜', '⬜', '⬜', '⬜' , '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬛', '⬜' , '⬛'],

    # ['⬛' , '🟥', '⬜', '⬜', '⬛', '⬜' , '⬛'],

    # ['⬛' , '🟦', '⬜', '⬜', '⬜', '⬜' , '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛' , '⬛'],
    # ]


    # 7 x 10
    # init_board =[
    # ['⬜' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛',  '⬜'],

    # ['⬛' , '⬛', '🔲🟧', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛',  '⬛'],

    # ['🔲⬛' , '🔲🟥', '⬜', '🟧', '⬜', '🟦', '⬜', '⬜', '⬜',  '⬛'],

    # ['🔲⬛' , '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜',  '⬛'],

    # ['⬛' , '🟥', '⬜', '⬜', '⬜', '⬜', '🔲🟦', '⬛', '⬜',  '⬛'],

    # ['⬛' , '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜',  '⬛'],

    # ['⬜' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛',  '⬛'],
    # ]


    # 8 x 11
    # init_board =[
    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜'],

    # ['⬛' , '🟥', '⬜', '⬛', '⬜', '⬜', '🟦', '⬛', '⬜', '⬜', '⬜'],

    # ['🔲⬛' , '⬜', '⬜', '🔲🟥', '⬜', '⬜', '⬜', '🔲⬛', '⬜', '⬜', '⬜'],

    # ['⬛' , '🔲🟧', '⬜', '⬜', '⬜', '🔲🟦', '⬜', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬛'],

    # ['⬜' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '🔲⬛', '⬜', '🟧', '⬛'],

    # ['⬜' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '🔲⬛', '⬛', '⬛'],
    # ]

 
    # Array size  5 x 12
    # init_board =[
    # ['⬜' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬛', '⬛', '⬜', '🔲🟦', '⬛'],

    # ['⬛' , '🔲⬜', '🔲🟩', '🔲🟧', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '🟩', '🟦', '🟧', '🟥', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]


    # 8 x 11
    # init_board =[
    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜'],

    # ['🔲⬛' , '🔲⬜', '🔲🟦', '⬜', '⬜', '⬜', '⬜', '🟥', '⬛', '⬜', '⬜'],

    # ['⬛' , '🔲🟩', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '🟦', '🟩', '⬜', '⬜', '⬜', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬜', '⬛', '⬛', '⬛', '⬜', '⬛', '⬜', '⬛'],

    # ['⬜' , '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬜' , '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]

    # 7 x 10
    # init_board =[
    # ['⬛' , '🔲⬛', '⬛', '⬛', '⬛', '🔲⬛', '⬛', '⬛', '🔲⬛',  '⬛'],

    # ['⬛' , '🔲⬜', '🟥', '⬜', '⬜', '🟦', '⬜', '🟧', '⬜',  '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '🔲🟥', '⬜',  '⬛'],

    # ['⬛' , '⬛', '⬜', '⬛', '⬛', '⬜', '⬛', '⬛', '⬜',  '⬛'],

    # ['⬜' , '⬛', '⬛', '⬛', '⬛', '⬜', '⬛', '⬛', '⬜',  '⬛'],

    # ['⬜' , '⬜', '⬜', '⬜', '⬛', '⬜', '⬜', '🔲🟧', '⬜',  '🔲⬛'],

    # ['⬜' , '⬜', '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛',  '⬛'],
    # ]

    # 10 x 12
    # init_board =[
    # ['⬜' , '⬜', '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜'],

    # ['⬜' , '⬜', '⬜', '⬜', '⬛', '⬛', '⬜', '🟥', '⬜', '⬛', '⬛', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '⬜', '🟧', '⬜', '⬜', '⬛'],

    # ['⬛' , '🟩', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬜', '⬛'],

    # ['⬛' , '🟦', '🔲🟦', '⬛', '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬜', '🔲⬜', '⬜', '⬛', '⬛', '⬛', '⬜', '⬛'],

    # ['⬜' , '⬜', '⬜', '⬛', '⬜', '🔲🟧', '⬜', '⬛', '⬛', '⬛', '⬜', '⬛'],

    # ['⬜' , '⬜', '⬜', '⬛', '⬜', '🔲🟥', '⬜', '⬜', '⬜', '⬜', '⬜', '🔲⬛'],

    # ['⬜' , '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]

    # 6 x 16
    init_board =[
    ['⬜' , '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜', '⬛', '⬛' , '⬛', '⬛', '⬛', '⬛'],

    ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬜', '⬜', '🔲🟨', '⬛', '⬛', '⬛', '🔲🟧' , '⬛', '⬛', '🔲🟩', '⬛'],

    ['⬛' , '🟥', '🟦', '🟩', '⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜' , '⬜', '⬜', '⬜', '⬛'],

    ['⬛' , '🟧', '🟨', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜' , '⬛', '⬜', '⬜', '⬛'],

    ['⬛' , '⬛', '⬛', '⬛', '⬛', '🔲⬜', '⬛', '⬛', '🔲🟦', '⬛', '⬛', '⬛' , '⬛', '⬛', '⬛', '⬛'],

    ['⬜' , '⬜', '⬜', '⬜', '⬛', '⬛', '⬛', '⬛', '🔲⬛', '⬛', '⬜', '⬜' , '⬜', '⬜', '⬜', '⬜'],
    ]


    # init_board =[
    #     ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛' , '⬛', '⬜' , '⬜'],

    #     ['⬛' , '⬜', '⬜', '⬜', '⬜', '🟦' , '⬛', '⬛' , '⬛'],

    #     ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜' , '⬛', '🔲🟧' , '⬛'],

    #     ['⬛' , '⬛', '⬛', '⬛', '⬜', '⬜' , '⬛', '⬜' , '⬛'],

    #     ['⬜' , '⬜', '⬛', '⬜', '⬜', '⬜' , '⬜', '⬜' , '⬛'],

    #     ['⬛' , '⬛', '⬛', '⬜', '⬛', '⬛' , '⬜', '⬜' , '⬛'],

    #     ['⬛' , '⬜', '⬜', '⬜', '⬛', '⬜' , '⬜', '⬜' , '⬛'],

    #     ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜' , '⬜', '⬜' , '⬛'],

    #     ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜' , '⬜', '🟧' , '⬛'],

    #     ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛' , '⬛', '🔲🟦' , '⬛'],

    #     ['⬜' , '⬜', '⬜', '⬜', '⬜', '⬜' , '⬛', '⬛' , '⬛'],
    #     ]


    #Array size  8 x 12
    # For Check the move Square procces
    # init_board =[
    # ['⬜' , '⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],

    # ['⬜' , '⬜', '⬛', '🟥', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '🔲🟧', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬜', '⬜', '⬜', '⬜', '🟩', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '🔲🟦', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬜', '⬜', '🟧', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '🔲🟥', '⬛'],

    # ['⬛' , '🔲🟩', '⬜', '⬜', '⬜', '⬜', '⬜', '🟦', '⬜', '⬜', '⬜', '⬛'],

    # ['⬛' , '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛', '⬛'],
    # ]


    
 


    rows = len(init_board)
    cols = len(init_board[0])
    board = [[None for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            if init_board[i][j] == '🟥':
                square_type = 'Red'
                role = 'Player'
                target_square = 'RedGoal'
                In_Place = False
            elif init_board[i][j] == '🟦':
                square_type = 'Blue'
                role = 'Player'
                target_square = 'BlueGoal'
                In_Place = False
            elif init_board[i][j] == '🟨':
               square_type = 'Yellow'
               role = 'Player'
               target_square = 'YellowGoal'
               In_Place = False
            elif init_board[i][j] == '🟩':
               square_type = 'Green'
               role = 'Player'
               target_square = 'GreenGoal'
               In_Place = False
            elif init_board[i][j] == '🟧':
               square_type = 'Orange'
               role = 'Player'
               target_square = 'OrangeGoal'
               In_Place = False
            elif init_board[i][j] == '🔲🟥':
               square_type = 'RedGoal'
               role = 'PlayerGoal'
               target_square = square_type
               In_Place = True
            elif init_board[i][j] == '🔲🟧':
               square_type = 'OrangeGoal'
               role = 'PlayerGoal'
               target_square = square_type
               In_Place = True
            elif init_board[i][j] == '🔲🟦':
               square_type = 'BlueGoal'
               role = 'PlayerGoal'
               target_square = square_type 
               In_Place = True
            elif init_board[i][j] == '🔲🟨':
               square_type = 'YellowGoal'
               role = 'PlayerGoal'
               target_square = square_type
               In_Place = True
            elif init_board[i][j] == '🔲🟩':
               square_type = 'GreenGoal'
               role = 'PlayerGoal'
               target_square = square_type
               In_Place = True
            elif init_board[i][j] == '⬛':
                square_type = 'Black'
                role = 'Block'
                target_square = ''
                In_Place = True
            elif init_board[i][j] == '🔲⬛':
                square_type = 'BlackWhite'
                role = 'LossBox'
                target_square = ''
                In_Place = True
            elif init_board[i][j] == '⬜':
               square_type = 'White'
               role = 'Crossing'
               target_square = '' 
               In_Place = True
            elif init_board[i][j] == '🔲⬜':
                square_type = 'WhiteWhite'
                role = 'VariableSquare'
                target_square = ''
                In_Place = True
            prev_type = square_type
            new_x = 0
            new_y = 0
            if(role == 'Player') :
                prev_type = 'White'
            board[i][j] = Square(i , j  , new_x , new_y , square_type,prev_type , role , target_square , In_Place ) 
    init_state = State(rows , cols , board)

    # print ("Parent_State is:")
    # print(init_state)
    # print("Children states are:")
    # Next_States = init_state.Get_Next_States()
    # for state in Next_States :
    #     print (state)


    main_menu(init_state)
 
    
if __name__ == '__main__':
    main()





