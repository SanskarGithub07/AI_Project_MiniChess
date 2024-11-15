import pygame
from piece2 import Rook, Knight, Bishop, Queen, King, Pawn

#class to represent the chessboard and managing its pieces
class ChessBoard:
    def __init__(self, screen, width, height):
        """
        Initializes the chessboard.
        screen - pygame screen to draw on
        width, height - dimensions of the board area
        tile_size - size of each square on the board
        board_offset_x, board_offset_y - offsets to center the board on the screen
        """
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
        """
        Sets up initial positions of all pieces for a standard chess game.
        Returns a list of piece instances with initial positions.
        """
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
        """
        Extracts a specific piece image from the full pieces image.
        piece_name - type of piece (e.g., 'queen')
        color - color of the piece ('white' or 'black')
        """
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
        """
        Draws the chessboard grid with alternating square colors.
        Also draws a border around the board.
        """ 
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
        """
        Draws all pieces on the board according to their current positions.
        Highlights pawns on their initial row.
        """
        for piece in self.pieces:
            piece.draw(self.tile_size, self.board_offset_x, self.board_offset_y)
            
            if isinstance(piece, Pawn):
                if ((piece.color == 'white' and piece.position[0] == 6) or 
                    (piece.color == 'black' and piece.position[0] == 1)):
                    x = self.board_offset_x + piece.position[1] * self.tile_size
                    y = self.board_offset_y + piece.position[0] * self.tile_size
                    pygame.draw.rect(self.screen, (255, 0, 0), 
                                (x, y, self.tile_size, self.tile_size), 2)

    def get_piece_at(self, position):
        """
        Finds and returns the piece at a given position, if one exists.
        position - tuple (row, col) of the target square
        """
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def move_piece(self, piece, new_position):
        """
        Attempts to move a piece to a new position.
        Returns True if the move is successful.
        """
        if piece and piece.move(new_position, self):
            return True
        return False
    
    def is_empty_square(self, row, col):
        """
        Checks if a square at given row and col is empty.
        Returns True if there is no piece at the square.
        """
        return self.get_piece_at((row, col)) is None

    def is_opponent_piece(self, row, col, current_color):
        """
        Checks if a piece at given coordinates belongs to the opponent.
        Returns True if the piece color is opposite to current_color.
        """
        piece = self.get_piece_at((row, col))
        return piece is not None and piece.color != current_color
    
    def draw_possible_moves(self, piece):
        """
        Highlights the possible moves for a given piece on the board.
        """
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
        """
        Converts a screen position (pixel coordinates) to board coordinates.
        position - tuple (x, y) of mouse click position
        Returns a tuple (row, col) representing the board coordinates.
        """
        tile_x = (position[0] - self.board_offset_x) // self.tile_size
        tile_y = (position[1] - self.board_offset_y) // self.tile_size
        return (tile_y, tile_x)
    
    def get_pieces_by_color(self, color):
        """
        Returns a list of pieces of a specific color.
        color - color of the pieces ('white' or 'black')
        """
        return [piece for piece in self.pieces if piece.color == color]
    
    def find_king(self, color):
        """
        Finds and returns the king piece of a specific color.
        color - color of the king ('white' or 'black')
        """
        for piece in self.pieces:
            if isinstance(piece, King) and piece.color == color:
                return piece
        return None
