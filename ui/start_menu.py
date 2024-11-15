import pygame
import sys

class StartMenu:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.buttons = {
            'new_game': pygame.Rect(screen_width//4, screen_height//4, screen_width//2, 50),
            'load_game': pygame.Rect(screen_width//4, screen_height//4 + 100, screen_width//2, 50),
            'delete_save': pygame.Rect(screen_width//4, screen_height//4 + 200, screen_width//2, 50)
        }
        self.game_mode_buttons = {
            'human_vs_human': pygame.Rect(screen_width//4, screen_height//4, screen_width//2, 50),
            'human_vs_ai': pygame.Rect(screen_width//4, screen_height//4 + 100, screen_width//2, 50),
            'ai_vs_ai': pygame.Rect(screen_width//4, screen_height//4 + 200, screen_width//2, 50),
            'back': pygame.Rect(screen_width//4, screen_height//4 + 300, screen_width//2, 50)
        }
        self.show_game_modes = False

    def draw_button(self, rect, text, hover=False):
        color = (100, 100, 100) if hover else (70, 70, 70)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.show_game_modes:
                        if self.buttons['new_game'].collidepoint(mouse_pos):
                            self.show_game_modes = True
                        elif self.buttons['load_game'].collidepoint(mouse_pos):
                            return 'load_game'
                        elif self.buttons['delete_save'].collidepoint(mouse_pos):
                            return 'delete_save'
                    else:
                        if self.game_mode_buttons['human_vs_human'].collidepoint(mouse_pos):
                            return 'human_vs_human'
                        elif self.game_mode_buttons['human_vs_ai'].collidepoint(mouse_pos):
                            return 'human_vs_ai'
                        elif self.game_mode_buttons['ai_vs_ai'].collidepoint(mouse_pos):
                            return 'ai_vs_ai'
                        elif self.game_mode_buttons['back'].collidepoint(mouse_pos):
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