import pygame
import sys
from chessboard import ChessBoard
from game_rules import GameRules
from sounds import SoundManager
from ui.start_menu import StartMenu
from ui.game_menu import GameMenu
from ui.status_display import StatusDisplay
from chess_ai import ChessAI

def main():
    pygame.init()
    sound_manager = SoundManager()
    
    # Screen setup
    board_width, board_height = 600, 600
    sidebar_width = 200
    screen_width = board_width + sidebar_width
    screen = pygame.display.set_mode((screen_width, board_height))
    pygame.display.set_caption('Chess Board')
    
    # Initialize start menu
    start_menu = StartMenu(screen_width, board_height)
    
    while True:
        # Show start menu and get selected option
        choice = start_menu.run()
        
        if choice == 'Human_vs_Human':
            run_game(screen, screen_width, board_height, sidebar_width, sound_manager)
        elif choice == 'Human_vs_AI':
            # To be implemented
            run_game(screen, screen_width, board_height, sidebar_width, sound_manager, 'Human_vs_AI')
        elif choice == 'AI_vs_AI':
            # To be implemented
            run_game(screen, screen_width, board_height, sidebar_width, sound_manager,'AI_vs_AI')

def run_game(screen, screen_width, board_height, sidebar_width, sound_manager, game_mode='Human_vs_Human'):
    board_width = screen_width - sidebar_width
    chess_board = ChessBoard(screen, board_width, board_height)
    game_rules = GameRules(chess_board)
    game_menu = GameMenu(screen_width, board_height, sidebar_width)
    clock = pygame.time.Clock()
    
    # Initialize AI if needed
    ai = None
    if game_mode in ['Human_vs_AI', 'AI_vs_AI']:
        ai = ChessAI(chess_board, game_rules, depth=3)
    
    running = True
    selected_piece = None
    status_display = StatusDisplay(board_width, board_height, sidebar_width)
    
    def draw_turn_indicator():
        sidebar_color = (0, 0, 0) if game_rules.current_turn == 'black' else (255, 255, 255)
        pygame.draw.rect(screen, sidebar_color, (board_width, 0, sidebar_width, board_height))
    
    def update_game_status():
        current_player = game_rules.current_turn
        opponent = 'white' if current_player == 'black' else 'black'
        
        if game_rules.is_in_check(current_player):
            # Find which piece is causing the check
            checking_piece = None
            opponent_pieces = chess_board.get_pieces_by_color(opponent)
            king_position = chess_board.find_king(current_player).position
            
            for piece in opponent_pieces:
                if king_position in piece.get_possible_moves(chess_board):
                    checking_piece = f"{opponent.capitalize()}'s {piece.__class__.__name__}"
                    break
            
            status_display.update_status(
                f"{current_player.capitalize()} is in Check!",
                "check",
                checking_piece
            )
    
    def handle_move(selected_piece, final_position):
        if game_rules.is_move_legal(selected_piece, final_position) and chess_board.move_piece(selected_piece, final_position):
            current_player = game_rules.current_turn
            opponent = 'white' if current_player == 'black' else 'black'
            
            if game_rules.is_in_check(current_player):
                # Find which piece is causing the check
                checking_piece = None
                opponent_pieces = chess_board.get_pieces_by_color(opponent)
                king_position = chess_board.find_king(current_player).position
                
                for piece in opponent_pieces:
                    if king_position in piece.get_possible_moves(chess_board):
                        checking_piece = f"{opponent.capitalize()}'s {piece.__class__.__name__}"
                        break
                
                status_display.update_status(
                    f"{current_player.capitalize()} is in Check!",
                    "check",
                    checking_piece
                )
                sound_manager.play_check_sound()
            
            game_over = game_rules.is_game_over()
            if game_over:
                if "Checkmate" in game_over:
                    status_display.update_status(game_over, "checkmate")
                    sound_manager.play_checkmate_sound()
                elif "Stalemate" in game_over:
                    status_display.update_status(game_over, "stalemate")
                    sound_manager.play_move_sound()
                else:
                    sound_manager.play_move_sound()
                return True
            else:
                sound_manager.play_move_sound()
            game_rules.switch_turn()
            return True
        return False
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle AI moves
        if ((game_mode == 'Human_vs_AI' and game_rules.current_turn == 'black') or 
            (game_mode == 'AI_vs_AI')):
            
            best_move = ai.get_best_move(game_rules.current_turn)
            if best_move:
                piece, new_position = best_move
                if handle_move(piece, new_position):
                    selected_piece = None
                    # Add a small delay to make AI moves visible
                    # pygame.time.wait(500)
                    continue
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_mode == 'AI_vs_AI':
                    continue
                # Check if menu icon is clicked
                menu_action = game_menu.handle_click(mouse_pos)
                if menu_action:
                    if menu_action == 'resume':
                        game_menu.menu_open = False
                    elif menu_action == 'save_game':
                        # Implement save game functionality here
                        pass
                    elif menu_action == 'main_menu':
                        return
                    continue
                
                if not game_menu.menu_open:
                    position = pygame.mouse.get_pos()
                    tile_position = chess_board.handle_click(position)
                    piece = chess_board.get_piece_at(tile_position) if tile_position else None
                    
                    if selected_piece is None:
                        if piece and piece.color == game_rules.current_turn:
                            selected_piece = piece
                    else:
                        if handle_move(selected_piece, tile_position):
                            selected_piece = None
                        elif piece and piece.color == game_rules.current_turn:
                            selected_piece = piece
                        else:
                            selected_piece = None
        
        # Clear screen for redraw
        screen.fill((255, 255, 255))
        chess_board.construct_board()
        
        # Highlight selected piece and possible moves
        if selected_piece:
            x = chess_board.board_offset_x + selected_piece.position[1] * chess_board.tile_size
            y = chess_board.board_offset_y + selected_piece.position[0] * chess_board.tile_size
            pygame.draw.rect(screen, (255, 255, 0), (x, y, chess_board.tile_size, chess_board.tile_size), 3)
            
            possible_moves = selected_piece.get_possible_moves(chess_board)
            for move in possible_moves:
                move_x = chess_board.board_offset_x + move[1] * chess_board.tile_size
                move_y = chess_board.board_offset_y + move[0] * chess_board.tile_size
                highlight_surface = pygame.Surface((chess_board.tile_size, chess_board.tile_size), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, (0, 255, 0, 128), highlight_surface.get_rect())
                screen.blit(highlight_surface, (move_x, move_y))
        
        # Draw all pieces
        chess_board.draw_pieces()
        
        # Draw UI elements
        draw_turn_indicator()
        update_game_status()
        status_display.draw(screen)
        game_menu.draw_menu(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()