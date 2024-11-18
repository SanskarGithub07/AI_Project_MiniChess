import pygame

class Popup:
    def __init__(self, screen, message, duration=2000):
        self.screen = screen
        self.message = message
        self.duration = duration
        self.start_time = None
        self.font = pygame.font.SysFont("Arial", 20)
        
        self.width = 200
        self.height = 50
        self.x = (screen.get_width() - self.width) // 2
        self.y = screen.get_height() - self.height - 20
        
    def show(self):
        self.start_time = pygame.time.get_ticks()
        
    def draw(self):
        if not self.start_time:
            return False
            
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            return False
            
        popup_surface = pygame.Surface((self.width, self.height))
        popup_surface.fill((50, 50, 50))
        pygame.draw.rect(popup_surface, (200, 200, 200), popup_surface.get_rect(), 2)
        
        text_surface = self.font.render(self.message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width//2, self.height//2))
        popup_surface.blit(text_surface, text_rect)
        
        self.screen.blit(popup_surface, (self.x, self.y))
        return True