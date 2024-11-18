import pygame
import sys

class GameMenu:
    def __init__(self, screen_width, screen_height, sidebar_width):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sidebar_width = sidebar_width
        self.font = pygame.font.Font(None, 36)
        
        icon_size = 30
        icon_x = screen_width - (sidebar_width / 2) - (icon_size / 2)
        self.menu_icon = pygame.Rect(icon_x, 10, icon_size, icon_size)
        
        self.menu_open = False
        self.buttons = {
        'resume': pygame.Rect(screen_width // 4, screen_height // 4, screen_width // 2, 50),
        'save_game': pygame.Rect(screen_width // 4, screen_height // 4 + 100, screen_width // 2, 50),
        'load_game': pygame.Rect(screen_width // 4, screen_height // 4 + 200, screen_width // 2, 50),
        'main_menu': pygame.Rect(screen_width // 4, screen_height // 4 + 300, screen_width // 2, 50)
        }


    def draw_menu_icon(self, screen):
        pygame.draw.rect(screen, (70, 70, 70), self.menu_icon, border_radius=5)
        
        for i in range(3):
            pygame.draw.line(screen, (255, 255, 255),
                           (self.menu_icon.left + 5, self.menu_icon.top + 7 + i * 8),
                           (self.menu_icon.right - 5, self.menu_icon.top + 7 + i * 8),
                           2)

    def draw_menu(self, screen):
        if self.menu_open:
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            screen.blit(overlay, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            for button_name, button_rect in self.buttons.items():
                hover = button_rect.collidepoint(mouse_pos)
                color = (100, 100, 100) if hover else (70, 70, 70)
                pygame.draw.rect(screen, color, button_rect, border_radius=5)
                pygame.draw.rect(screen, (200, 200, 200), button_rect, 2, border_radius=5)
                text_surface = self.font.render(button_name.replace('_', ' ').title(), True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=button_rect.center)
                screen.blit(text_surface, text_rect)
        else:
            self.draw_menu_icon(screen)

    def handle_click(self, pos):
        if self.menu_icon.collidepoint(pos):
            self.menu_open = not self.menu_open
            return None
        
        if self.menu_open:
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(pos):
                    return button_name
        return None