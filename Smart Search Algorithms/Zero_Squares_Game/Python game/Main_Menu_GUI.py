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