import pygame

class Piece:
    def __init__(self, screen, image, color, position):
        self.screen = screen
        self.image = image
        self.color = color
        self.position = position

    def draw(self, tile_size, board_offset_x, board_offset_y):
        x = board_offset_x + self.position[1] * tile_size
        y = board_offset_y + self.position[0] * tile_size
        self.screen.blit(self.image, (x, y))

    def move(self, new_position):
        self.position = new_position

class Rook(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

class Knight(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

class Bishop(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

class Queen(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

class King(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

class Pawn(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)
