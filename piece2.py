import pygame

#base class for chess pieces
class Piece:
    
    def __init__(self, screen, image, color, position):
        """
        Initializes a chess piece with essential attributes:
        screen - surface on which the piece will be drawn
        image - visual representation of the piece
        color - piece color ('white' or 'black')
        position - tuple for piece's current board coordinates (row, col)
        type - type of piece (e.g., 'pawn', 'rook', 'knight')
        """
        self.screen = screen
        self.image = image
        self.color = color
        self.position = position
        self.type = self.__class__.__name__.lower()

    def draw(self, tile_size, board_offset_x, board_offset_y):
        """
        Draws the piece on the screen at its current position.
        tile_size - size of each square on the board
        board_offset_x, board_offset_y - pixel offset for the board's top-left corner
        """
        x = board_offset_x + self.position[1] * tile_size
        y = board_offset_y + self.position[0] * tile_size
        self.screen.blit(self.image, (x, y))
    
    def move(self, new_position, board):
        """
        Moves the piece to a new position if the move is valid.
        new_position - tuple for target coordinates (row, col)
        board - current game board instance
        """
        if self.is_valid_move(new_position, board):
            target_piece = board.get_piece_at(new_position)
            if target_piece:
                board.pieces.remove(target_piece)

            self.position = new_position
            self.moved_once = True

            if isinstance(self, Pawn):  ## Check if the piece is a pawn
                self.check_promotion(new_position, board)   

            return True
        return False

    ## Only for the pawn -> queen change
    def check_promotion(self, new_position, board):
        """
        Checks if the pawn has reached the end of the board for promotion.
        Only applies to pawns, which are promoted to a queen.
        """
        if (self.color == 'white' and new_position[0] == 7) or \
        (self.color == 'black' and new_position[0] == 0):
            self.promote(board)
    
    def is_valid_move(self, new_position, board):
        """
        Validates the move by checking if it’s in the piece's possible moves.
        """
        if new_position not in self.get_possible_moves(board):
            return False
        return True
    
    def get_possible_moves(self, board):
        """
        Returns a list of possible moves for the piece based on its type.
        Uses movement patterns for each piece type to calculate valid moves.
        """
        possible_moves = []
        current_row, current_col = self.position

        # Define the movement patterns for different piece types
        movement_patterns = {
            'rook': [(-1, 0), (1, 0), (0, -1), (0, 1)],
            'knight': [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)],
            'bishop': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            'queen': [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (1, 0), (-1, 0), (0, -1)],
            'king': [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 1), (1, 0), (-1, 0), (0, -1)],
            'pawn': [(1, 0)]
        }

        for direction in movement_patterns[self.type]:
            possible_moves.extend(self.get_moves_in_direction(board, current_row, current_col, direction))

        return possible_moves
    
    def get_moves_in_direction(self, board, row, col, direction):
        """
        Generates moves in a specific direction (used for rooks, bishops, queens).
        Stops if blocked by another piece or after a capture.
        """
        moves = []
        row_increase, col_increase = direction
        new_row, new_col = row + row_increase, col + col_increase

        if self.type in ['rook', 'bishop', 'queen']:
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.is_empty_square(new_row, new_col) or board.is_opponent_piece(new_row, new_col, self.color):
                    moves.append((new_row, new_col))
                    if board.is_opponent_piece(new_row, new_col, self.color):
                        break  # Stop checking after capturing
                else:
                    break  # Stop checking if blocked by a friendly piece

                new_row += row_increase
                new_col += col_increase
        else:
            # For knight and king, directly add move if valid
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.is_empty_square(new_row, new_col) or board.is_opponent_piece(new_row, new_col, self.color):
                    moves.append((new_row, new_col))

        return moves

class Rook(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass    

class Queen(Piece):
    pass

class King(Piece):
    pass
        
class Pawn(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)
        self.moved_once = False
        self.direction = 1 if color == 'white' else -1
            
    def get_possible_moves(self, board):
        """
        Overrides get_possible_moves for pawn-specific movement rules.
        Pawns can move forward, and capture diagonally.
        """
        possible_moves = []
        current_row, current_col = self.position
        new_row = current_row + self.direction
        if 0 <= new_row < 8:
            
            if not board.get_piece_at((new_row, current_col)):
                possible_moves.append((new_row, current_col))
                
                ## En passant by checking if the pawn has moved once using boolean flag
                if not self.moved_once:
                    second_row_ahead =  current_row + (2 * self.direction)               
                    if (0 <= second_row_ahead < 8 and not board.get_piece_at((second_row_ahead, current_col))):
                        possible_moves.append((second_row_ahead, current_col)) 
                                 
        capture_squares = [
            (new_row, current_col - 1),
            (new_row, current_col + 1)
        ]        
        
        for capture_square in capture_squares:
            c_row, c_col = capture_square
            if 0 <= c_row < 8 and 0 <= c_col < 8:
                target_piece = board.get_piece_at((capture_square))
                if target_piece and target_piece.color != self.color:
                    possible_moves.append(capture_square)
                    
        return possible_moves
    
    def promote(self, board):
        """
        Promotes a pawn to a queen upon reaching the farthest row.
        """
        board.pieces.remove(self)
        
        queen_image = board.get_piece_image('queen', self.color)
        new_queen = Queen(self.screen, queen_image, self.color, self.position)
        board.pieces.append(new_queen)
     