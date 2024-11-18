from piece2 import King, Queen, Rook, Bishop, Knight, Pawn
import time

class ChessAI:
    def __init__(self, board, game_rules, depth=3):
        self.board = board
        self.game_rules = game_rules
        self.depth = depth
        
        self.piece_values = {
            'pawn': 100,
            'knight': 320,
            'bishop': 330,
            'rook': 500,
            'queen': 900,
            'king': 20000
        }
        
        self.pawn_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        
        self.knight_table = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]
        
        self.bishop_table = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]
        
        self.rook_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]
        ]
        
        self.queen_table = [
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ]
        
        self.king_table = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [20, 30, 10,  0,  0, 10, 30, 20]
        ]

    def get_best_move(self, color):
        """Returns the best move for the given color using minimax with alpha-beta pruning."""
        self.positions_evaluated = 0  # Reset counter
        start_time = time.time()  # Start timing
        
        best_value = float('-inf') if color == 'white' else float('inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        pieces = [p for p in self.board.pieces if p.color == color]
        
        for piece in pieces:
            possible_moves = piece.get_possible_moves(self.board)
            for move in possible_moves:
                if self.game_rules.is_move_legal(piece, move):
                    self.positions_evaluated += 1  # Increment counter
                    old_pos = piece.position
                    captured_piece = self.board.get_piece_at(move)
                    if captured_piece:
                        self.board.pieces.remove(captured_piece)
                    piece.position = move
                    
                    if color == 'white':
                        value = self.minimax(self.depth - 1, alpha, beta, False)
                        if value > best_value:
                            best_value = value
                            best_move = (piece, move)
                        alpha = max(alpha, value)
                    else:
                        value = self.minimax(self.depth - 1, alpha, beta, True)
                        if value < best_value:
                            best_value = value
                            best_move = (piece, move)
                        beta = min(beta, value)
                    
                    piece.position = old_pos
                    if captured_piece:
                        self.board.pieces.append(captured_piece)
                    
                    if alpha >= beta:
                        break
        
        evaluation_time = time.time() - start_time  # Calculate time taken
    
        # Update status display with AI statistics
        if hasattr(self, 'status_display'):
            self.status_display.update_ai_stats(
                self.depth,
                self.positions_evaluated,
                evaluation_time
            )
        
        return best_move

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game_rules.is_game_over():
            return self.evaluate_position()
        
        if maximizing_player:
            max_eval = float('-inf')
            pieces = [p for p in self.board.pieces if p.color == 'white']
            
            for piece in pieces:
                possible_moves = piece.get_possible_moves(self.board)
                for move in possible_moves:
                    if self.game_rules.is_move_legal(piece, move):
                        old_pos = piece.position
                        captured_piece = self.board.get_piece_at(move)
                        if captured_piece:
                            self.board.pieces.remove(captured_piece)
                        piece.position = move
                        
                        eval = self.minimax(depth - 1, alpha, beta, False)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        
                        piece.position = old_pos
                        if captured_piece:
                            self.board.pieces.append(captured_piece)
                        
                        if beta <= alpha:
                            break
                            
            return max_eval
        else:
            min_eval = float('inf')
            pieces = [p for p in self.board.pieces if p.color == 'black']
            
            for piece in pieces:
                possible_moves = piece.get_possible_moves(self.board)
                for move in possible_moves:
                    if self.game_rules.is_move_legal(piece, move):
                        old_pos = piece.position
                        captured_piece = self.board.get_piece_at(move)
                        if captured_piece:
                            self.board.pieces.remove(captured_piece)
                        piece.position = move
                        
                        eval = self.minimax(depth - 1, alpha, beta, True)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        
                        piece.position = old_pos
                        if captured_piece:
                            self.board.pieces.append(captured_piece)
                        
                        if beta <= alpha:
                            break
                            
            return min_eval

    def evaluate_position(self):
        total_eval = 0
        
        for piece in self.board.pieces:
            piece_value = self.piece_values[piece.type]
            position_value = self.get_position_value(piece)
            
            if piece.color == 'white':
                total_eval += piece_value + position_value
            else:
                total_eval -= piece_value + position_value
                
        return total_eval
    
    def get_position_value(self, piece):
        row, col = piece.position
        if piece.color == 'black':
            row = 7 - row  # Flip the table for black pieces
            
        position_tables = {
            'pawn': self.pawn_table,
            'knight': self.knight_table,
            'bishop': self.bishop_table,
            'rook': self.rook_table,
            'queen': self.queen_table,
            'king': self.king_table
        }
        
        return position_tables[piece.type][row][col]