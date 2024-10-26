import pygame
from piece2 import Rook, Knight, Bishop, Queen, King, Pawn

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
        self.pieces_image = pygame.image.load('Pieces/ChessPiecesArray.png').convert_alpha()
        self.piece_size = self.pieces_image.get_height() // 2

        # Initialize pieces
        self.pieces = self.initialize_pieces()

    def initialize_pieces(self):
        pieces = []
        # Initial positions for white pieces
        white_positions = {
            Rook: [(0, 0), (0, 7)],
            Knight: [(0, 1), (0, 6)],
            Bishop: [(0, 2), (0, 5)],
            Queen: [(0, 3)],
            King: [(0, 4)],
            Pawn: [(1, col) for col in range(8)]
        }
        # Initial positions for black pieces
        black_positions = {
            Rook: [(7, 0), (7, 7)],
            Knight: [(7, 1), (7, 6)],
            Bishop: [(7, 2), (7, 5)],
            Queen: [(7, 3)],
            King: [(7, 4)],
            Pawn: [(6, col) for col in range(8)]
        }
        # Create white pieces
        for piece_class, positions in white_positions.items():
            for position in positions:
                piece_image = self.get_piece_image(piece_class.__name__.lower(), 'white')
                pieces.append(piece_class(self.screen, piece_image, 'white', position))
        # Create black pieces
        for piece_class, positions in black_positions.items():
            for position in positions:
                piece_image = self.get_piece_image(piece_class.__name__.lower(), 'black')
                pieces.append(piece_class(self.screen, piece_image, 'black', position))
        return pieces

    def get_piece_image(self, piece_name, color):
        row = 0 if color == 'black' else 1
        col = {
            'king': 1,
            'queen': 0,
            'rook': 2,
            'knight': 3,
            'bishop': 4,
            'pawn': 5
        }[piece_name]
        return self.pieces_image.subsurface(
            col * self.piece_size, row * self.piece_size, self.piece_size, self.piece_size
        )

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

    def draw_pieces(self):
        for piece in self.pieces:
            piece.draw(self.tile_size, self.board_offset_x, self.board_offset_y)
            
            if isinstance(piece, Pawn):
                if ((piece.color == 'white' and piece.position[0] == 6) or 
                    (piece.color == 'black' and piece.position[0] == 1)):
                    x = self.board_offset_x + piece.position[1] * self.tile_size
                    y = self.board_offset_y + piece.position[0] * self.tile_size
                    pygame.draw.rect(self.screen, (255, 215, 0), 
                                (x, y, self.tile_size, self.tile_size), 2)

    def get_piece_at(self, position):
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def move_piece(self, piece, new_position):
        if piece.move(new_position, self):
            return True
        return False
    
    def is_empty_square(self, row, col):
        return self.get_piece_at((row, col)) is None

    def is_opponent_piece(self, row, col, current_color):
        piece = self.get_piece_at((row, col))
        return piece is not None and piece.color != current_color
    
    def draw_possible_moves(self, piece):
        if piece:
            possible_moves = piece.get_possible_moves(self)
            highlight_color = (124, 252, 0, 128)
            surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            pygame.draw.rect(surface, highlight_color, surface.get_rect())
            
            for move in possible_moves:
                x = self.board_offset_x + move[1] * self.tile_size
                y = self.board_offset_y + move[0] * self.tile_size
                self.screen.blit(surface, (x, y))

    def handle_click(self, position):
        tile_x = (position[0] - self.board_offset_x) // self.tile_size
        tile_y = (position[1] - self.board_offset_y) // self.tile_size
        return (tile_y, tile_x)
