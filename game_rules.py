from piece2 import King

class GameRules:
    def __init__(self, board):
        self.board = board
        self.current_turn = 'white'

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def is_in_check(self, color):
        king = next((piece for piece in self.board.pieces if isinstance(piece, King) and piece.color == color), None)
        if not king:
            return False

        king_pos = king.position
        opponent_pieces = [p for p in self.board.pieces if p.color != color]

        for piece in opponent_pieces:
            if king_pos in piece.get_possible_moves(self.board):
                return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        pieces = [p for p in self.board.pieces if p.color == color]
        for piece in pieces:
            possible_moves = piece.get_possible_moves(self.board)
            original_position = piece.position
            for move in possible_moves:
                # Simulate the move
                target_piece = self.board.get_piece_at(move)
                piece.position = move
                if target_piece:
                    self.board.pieces.remove(target_piece)

                if not self.is_in_check(color):
                    # Undo the move and return False (not a checkmate)
                    piece.position = original_position
                    if target_piece:
                        self.board.pieces.append(target_piece)
                    return False

                # Undo the move
                piece.position = original_position
                if target_piece:
                    self.board.pieces.append(target_piece)

        return True

    def is_stalemate(self, color):
        if self.is_in_check(color):
            return False

        pieces = [p for p in self.board.pieces if p.color == color]
        for piece in pieces:
            if piece.get_possible_moves(self.board):
                return False
        return True

    def is_game_over(self):
        if self.is_checkmate(self.current_turn):
            return f"Checkmate! {self.current_turn} loses."
        elif self.is_stalemate(self.current_turn):
            return "Stalemate! It's a draw."
        return None
