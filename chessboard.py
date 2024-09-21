import pygame

class ChessBoard:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.tile_size = min(width, height) // 8
        self.board_offset_x = (width - self.tile_size * 8) // 2
        self.board_offset_y = (height - self.tile_size * 8) // 2
        self.light_color = (240, 217, 181)
        self.dark_color = (181, 136, 99)
        
    def construct_board(self):
        for row in range(8):
            for col in range(8):
                x = self.board_offset_x + col * self.tile_size
                y = self.board_offset_y + row * self.tile_size
                color = self.dark_color
                if (row + col) % 2 == 0:
                    color = self.light_color
                pygame.draw.rect(self.screen, color, (x, y, self.tile_size, self.tile_size))
        
        border_color = (0, 0, 0)
        border_width = 2
        pygame.draw.rect(self.screen, border_color, 
            (self.board_offset_x - border_width,
            self.board_offset_y - border_width,
            self.tile_size * 8 + border_width * 2,
            self.tile_size * 8 + border_width * 2),
            border_width)
                

        
        