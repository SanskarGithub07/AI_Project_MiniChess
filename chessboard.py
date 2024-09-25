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
        
        # Load the chess pieces image
        self.pieces_image = pygame.image.load('ChessPiecesArray.png').convert_alpha()
        self.piece_size = self.pieces_image.get_height() // 2

        # Define the piece positions in the image
        self.pieces = {
            'black': {
                'queen': (0, 0),
                'king': (1, 0),
                'rook': (2, 0),
                'knight': (3, 0),
                'bishop': (4, 0),
                'pawn': (5, 0),
            },
            'white': {
                'queen': (0, 1),
                'king': (1, 1),
                'rook': (2, 1),
                'knight': (3, 1),
                'bishop': (4, 1),
                'pawn': (5, 1),
            }
        }

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

    def draw_piece(self, piece_name, color, position):
        col, row = self.pieces[color][piece_name]
        piece_image = self.pieces_image.subsurface(
            col * self.piece_size, row * self.piece_size, self.piece_size, self.piece_size
        )
        x = self.board_offset_x + position[1] * self.tile_size
        y = self.board_offset_y + position[0] * self.tile_size
        self.screen.blit(piece_image, (x, y))

    def draw_pieces(self):
        # Initial positions for white pieces
        white_positions = {
            'rook': [(0, 0), (0, 7)],
            'knight': [(0, 1), (0, 6)],
            'bishop': [(0, 2), (0, 5)],
            'queen': [(0, 3)],
            'king': [(0, 4)],
            'pawn': [(1, col) for col in range(8)]
        }
        # Initial positions for black pieces
        black_positions = {
            'rook': [(7, 0), (7, 7)],
            'knight': [(7, 1), (7, 6)],
            'bishop': [(7, 2), (7, 5)],
            'queen': [(7, 3)],
            'king': [(7, 4)],
            'pawn': [(6, col) for col in range(8)]
        }
        # Draw white pieces
        for piece_name, positions in white_positions.items():
            for position in positions:
                self.draw_piece(piece_name, 'white', position)
        # Draw black pieces
        for piece_name, positions in black_positions.items():
            for position in positions:
                self.draw_piece(piece_name, 'black', position)


