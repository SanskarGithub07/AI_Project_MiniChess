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
        
    def get_possible_moves(self, board):
        possible_moves = []
        current_row, current_col = self.position
        
        # Bishop movement diagonal directions
        directions = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]
        
        for direction in directions:
            row_increase, col_increase = direction
            new_row = current_row + row_increase
            new_col = current_col + col_increase
            
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece_at((new_row, new_col))
                
                # if target_piece is None:
                possible_moves.append((new_row, new_col))
                    
                # elif target_piece.color != self.color:
                #     possible_moves.append((new_row, new_col))
                #     break
                
                # else:
                #     break
                
                new_row += row_increase
                new_col += col_increase
                
        return possible_moves

    def is_valid_move(self, new_position, board):
        if new_position not in self.get_possible_moves(board):
            return False
        return True
    
    def move(self, new_position, board):
        if self.is_valid_move(new_position, board):
            # target_piece = board.get_piece_at(new_position, board)
            # if target_piece:
            #     board.pieces.remove(target_piece)
            
            self.position = new_position
            return True
        return False

class Queen(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

class King(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

class Pawn(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)
        
                
