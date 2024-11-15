import pygame
import sys

class StartMenu:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = pygame.font.SysFont("Segoe UI", size = 72) 
        self.button_font = pygame.font.SysFont("Segoe UI", size = 32)  

        self.button_color = (50, 150, 255) 
        self.hover_color = (100, 200, 255) 
        
        self.buttons = {
            'New_game': pygame.Rect(screen_width//4, screen_height//4, screen_width//2, 60),  
            'Load_game': pygame.Rect(screen_width//4, screen_height//4 + 120, screen_width//2, 60), 
            'Delete_save': pygame.Rect(screen_width//4, screen_height//4 + 240, screen_width//2, 60) 
        }
        self.game_mode_buttons = {
            'Human_vs_Human': pygame.Rect(screen_width//4, screen_height//4, screen_width//2, 60),
            'Human_vs_AI': pygame.Rect(screen_width//4, screen_height//4 + 120, screen_width//2, 60), 
            'AI_vs_AI': pygame.Rect(screen_width//4, screen_height//4 + 240, screen_width//2, 60), 
            'Back': pygame.Rect(screen_width//4, screen_height//4 + 360, screen_width//2, 60) 
        }
        self.show_game_modes = False

    def draw_button(self, rect, text, hover=False):
        color = self.hover_color if hover else self.button_color
        pygame.draw.rect(self.screen, color, rect, border_radius=15)  # Rounded corners
        text_surface = self.button_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_gradient_background(self):
        """Draws a vertical gradient background."""
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            color = (int(30 * ratio), int(30 * ratio), int(60 * (1 - ratio)))  # Dark blue to almost black
            pygame.draw.line(self.screen, color, (0, y), (self.screen_width, y))

    # def draw_title(self, text):
    #     """Draws the title text."""
    #     text_surface = self.title_font.render(text, True, (255, 255, 255))
    #     text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 8))
    #     self.screen.blit(text_surface, text_rect)

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.show_game_modes:
                        if self.buttons['New_game'].collidepoint(mouse_pos):
                            self.show_game_modes = True
                        elif self.buttons['Load_game'].collidepoint(mouse_pos):
                            return 'Load_game'
                        elif self.buttons['Delete_save'].collidepoint(mouse_pos):
                            return 'Delete_save'
                    else:
                        if self.game_mode_buttons['Human_vs_Human'].collidepoint(mouse_pos):
                            return 'Human_vs_Human'
                        elif self.game_mode_buttons['Human_vs_AI'].collidepoint(mouse_pos):
                            return 'Human_vs_AI'
                        elif self.game_mode_buttons['AI_vs_AI'].collidepoint(mouse_pos):
                            return 'AI_vs_AI'
                        elif self.game_mode_buttons['Back'].collidepoint(mouse_pos):
                            self.show_game_modes = False

            self.screen.fill((30, 30, 30))
            
            if not self.show_game_modes:
                for button_name, button_rect in self.buttons.items():
                    hover = button_rect.collidepoint(mouse_pos)
                    self.draw_button(button_rect, button_name.replace('_', ' ').title(), hover)
            else:
                for button_name, button_rect in self.game_mode_buttons.items():
                    hover = button_rect.collidepoint(mouse_pos)
                    self.draw_button(button_rect, button_name.replace('_', ' ').title(), hover)

            pygame.display.flip()