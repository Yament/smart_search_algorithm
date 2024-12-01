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