from piece2 import King

class GameRules:
    def __init__(self, board):
        self.board = board
        self.current_turn = 'white'

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def is_in_check(self, color):
        """Check if the current player's king is in check."""
        king = next((piece for piece in self.board.pieces if isinstance(piece, King) and piece.color == color), None)
        if not king:
            return False

        king_pos = king.position
        opponent_pieces = [p for p in self.board.pieces if p.color != color]

        for piece in opponent_pieces:
            if king_pos in piece.get_possible_moves(self.board):
                return True
        return False

    def is_move_legal(self, piece, destination):
        """Ensure a piece's move doesn't place its own king in check."""
        initial_position = piece.position
        target_piece = self.board.get_piece_at(destination)
        
        # Simulate the move
        piece.position = destination
        if target_piece:
            self.board.pieces.remove(target_piece)
        
        in_check = self.is_in_check(piece.color)
        
        # Undo the move
        piece.position = initial_position
        if target_piece:
            self.board.pieces.append(target_piece)
        
        # Move is only legal if it does not put the king in check
        return not in_check

    def is_checkmate(self, color):
        """Check if the current player is in checkmate."""
        if not self.is_in_check(color):
            return False

        pieces = [p for p in self.board.pieces if p.color == color]
        for piece in pieces:
            possible_moves = piece.get_possible_moves(self.board)
            for move in possible_moves:
                if self.is_move_legal(piece, move):
                    return False  # If any legal move exists, it's not checkmate
        return True

    def is_stalemate(self, color):
        """Check for stalemate."""
        if self.is_in_check(color):
            return False

        pieces = [p for p in self.board.pieces if p.color == color]
        for piece in pieces:
            possible_moves = piece.get_possible_moves(self.board)
            for move in possible_moves:
                if self.is_move_legal(piece, move):
                    return False  # If any legal move exists, it's not stalemate
        return True

    def is_game_over(self):
        """Check if the game has ended with checkmate or stalemate."""
        if self.is_checkmate(self.current_turn):
            return f"Checkmate! {self.current_turn} loses."
        elif self.is_stalemate(self.current_turn):
            return "Stalemate! It's a draw."
        return None
