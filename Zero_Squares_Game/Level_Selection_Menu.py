
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
                                return i + 1
                elif event.type == pygame.MOUSEWHEEL:
                    # Scroll logic
                    self.scroll_offset += event.y * 20  # Adjust scroll speed
                    self.scroll_offset = max(min(self.scroll_offset, 0), -(scroll_area_height - WINDOW_HEIGHT))

            pygame.display.flip()
            # clock.tick(30)