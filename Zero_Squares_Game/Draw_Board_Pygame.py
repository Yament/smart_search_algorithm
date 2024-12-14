
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
                elif tile.type == 'GreenYellow':
                    pygame.draw.rect(screen, YELLOW, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, GREEN, (x, y, TILE_SIZE, TILE_SIZE),4) 
                elif tile.type == 'OrangeGreen':
                    pygame.draw.rect(screen, GREEN, (x, y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, ORANGE, (x, y, TILE_SIZE, TILE_SIZE),4)
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
     