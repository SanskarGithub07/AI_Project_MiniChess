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

    def move(self, new_position, board):
        if self.is_valid_move(new_position, board):
            self.position = new_position
            return True
        return False
    
    def is_valid_move(self, new_position, board):
        if new_position not in self.get_possible_moves(board):
            return False
        return True

class Rook(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

    def get_possible_moves(self, board):
        possible_moves = []
        current_row, current_col = self.position
        
        # Rook movement cardinal directions
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]
        
        for direction in directions:
            row_increase, col_increase = direction
            new_row = current_row + row_increase
            new_col = current_col + col_increase
            
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                possible_moves.append((new_row, new_col))
                new_row += row_increase
                new_col += col_increase
                
        return possible_moves

class Knight(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

    def get_possible_moves(self, board):
        possible_moves = []
        current_row, current_col = self.position
        
        # Knight movement - 8 directions
        directions = [
            (-2, -1),
            (-2, 1),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
            (-1, -2),
            (-1, 2)
        ]
        
        # Creates possible moves based on directions
        for direction in directions:
            row_increase, col_increase = direction
            new_row = current_row + row_increase
            new_col = current_col + col_increase
            
            # Clips it for 8x8 board and append
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                possible_moves.append((new_row, new_col))
                
        return possible_moves


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

    

class Queen(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

class King(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)

class Pawn(Piece):
    def __init__(self, screen, image, color, position):
        super().__init__(screen, image, color, position)
        self.moved_once = False
        self.direction = 1 if color == 'white' else -1
            
    def get_possible_moves(self, board):
        possible_moves = []
        current_row, current_col = self.position
        
        new_row = current_row + self.direction
        
        if 0 <= new_row < 8:
            
            if not board.get_piece_at((new_row, current_col)):
                possible_moves.append((new_row, current_col))
                
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
    
    # def is_valid_move(self, new_position, board):
    #     return new_position in self.get_possible_moves(board)
    
    def move(self, new_position, board):
        if self.is_valid_move(new_position, board):
            target_piece = board.get_piece_at(new_position)
            if target_piece:
                board.pieces.remove(target_piece)
                
            self.position = new_position
            self.moved_once = True
            
            if (self.color == 'white' and new_position[0] == 7) or \
               (self.color == 'black' and new_position[0] == 0):
                self.promote(board)
            
            return True
        return False
    
    def promote(self, board):
        board.pieces.remove(self)
        
        queen_image = board.get_piece_image('queen', self.color)
        new_queen = Queen(self.screen, queen_image, self.color, self.position)
        board.pieces.append(new_queen)
     
                  
    
