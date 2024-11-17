import pygame
import sys
from chessboard import ChessBoard
from game_rules import GameRules
from sounds import SoundManager
from ui.start_menu import StartMenu
from ui.game_menu import GameMenu
from ui.status_display import StatusDisplay
from chess_ai import ChessAI
import pickle

def save_game(chess_board, game_rules, game_mode, file_name="saved_game.pkl"):
    """
    Save the current game state to a file.
    """
    with open(file_name, 'wb') as file:
        game_state = {
            'board': [(p.type, p.color, p.position) for p in chess_board.pieces],
            'current_turn': game_rules.current_turn,
            'game_mode': game_mode  # Include game mode
        }
        pickle.dump(game_state, file)


def load_game(chess_board, game_rules, current_game_mode, file_name="saved_game.pkl"):
    """
    Load a saved game state from a file.
    """
    try:
        with open(file_name, 'rb') as file:
            game_state = pickle.load(file)
            
            # Check if the game mode matches
            saved_game_mode = game_state.get('game_mode', 'human_vs_human')  # Default if missing
            if saved_game_mode != current_game_mode:
                print(f"Error: Cannot load a {saved_game_mode} game in {current_game_mode} mode.")
                return False  # Indicate loading failure

            # Load the game state
            chess_board.pieces = [
                chess_board.create_piece(piece_type, color, position)
                for piece_type, color, position in game_state['board']
            ]
            game_rules.current_turn = game_state['current_turn']
            return True  # Indicate loading success
    except FileNotFoundError:
        print("No saved game found!")
        return False  # Indicate loading failure


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
            run_game(screen, screen_width, board_height, sidebar_width, sound_manager, 'human_vs_human')
        elif choice == 'Human_vs_AI':
            # To be implemented
            run_game(screen, screen_width, board_height, sidebar_width, sound_manager, 'Human_vs_AI')
        elif choice == 'AI_vs_AI':
            # To be implemented
            run_game(screen, screen_width, board_height, sidebar_width, sound_manager,'AI_vs_AI')

import threading
import time

def run_game(screen, screen_width, board_height, sidebar_width, sound_manager, game_mode='Human_vs_Human'):
    board_width = screen_width - sidebar_width
    chess_board = ChessBoard(screen, board_width, board_height)
    game_rules = GameRules(chess_board)
    game_menu = GameMenu(screen_width, board_height, sidebar_width)
    clock = pygame.time.Clock()

    # Initialize AIs
    ai_white = ChessAI(chess_board, game_rules, depth=3) if game_mode == 'AI_vs_AI' else None
    ai_black = ChessAI(chess_board, game_rules, depth=3) if game_mode in ['Human_vs_AI', 'AI_vs_AI'] else None

    # Synchronization variables
    ai_move_results = {'white': None, 'black': None}
    turn_lock = threading.Lock()
    ai_move_ready = threading.Event()

    def calculate_ai_move(ai, color):
        """AI computation runs in a separate thread."""
        best_move = ai.get_best_move(color)
        with turn_lock:
            ai_move_results[color] = best_move
            ai_move_ready.set()  # Signal that the move is ready

    running = True
    selected_piece = None
    status_display = StatusDisplay(board_width, board_height, sidebar_width)

    def draw_turn_indicator():
        sidebar_color = (0, 0, 0) if game_rules.current_turn == 'black' else (255, 255, 255)
        pygame.draw.rect(screen, sidebar_color, (board_width, 0, sidebar_width, board_height))

    def update_game_status():
     current_player = game_rules.current_turn
     opponent = 'white' if current_player == 'black' else 'black'

    # Check for game over first
     game_over = game_rules.is_game_over()
     if game_over:
        if "Checkmate" in game_over:
            status_display.update_status(game_over, "checkmate")
            sound_manager.play_checkmate_sound()
        elif "Stalemate" in game_over:
            status_display.update_status(game_over, "stalemate")
            sound_manager.play_move_sound()
        return  # Exit early to avoid overriding game-over status

    # Check for "Check" status
     if game_rules.is_in_check(current_player):
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

     current_player = game_rules.current_turn
     opponent = 'white' if current_player == 'black' else 'black'

    # Check for game over first
     game_over = game_rules.is_game_over()
     if game_over:
        if "Checkmate" in game_over:
            status_display.update_status(game_over, "checkmate")
            sound_manager.play_checkmate_sound()
        elif "Stalemate" in game_over:
            status_display.update_status(game_over, "stalemate")
            sound_manager.play_move_sound()
        return  # Exit early to avoid overriding game-over status

    # Check for "Check" status
     if game_rules.is_in_check(current_player):
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

        # Check if the game is over first
        game_over = game_rules.is_game_over()
        if game_over:
            if "Checkmate" in game_over:
                status_display.update_status(game_over, "checkmate")
                sound_manager.play_checkmate_sound()
            elif "Stalemate" in game_over:
                status_display.update_status(game_over, "stalemate")
                sound_manager.play_move_sound()
            return True

        # Check for "Check" status
        if game_rules.is_in_check(current_player):
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

        game_rules.switch_turn()
        sound_manager.play_move_sound()
        return True
     return False
    #  if game_rules.is_move_legal(selected_piece, final_position) and chess_board.move_piece(selected_piece, final_position):
    #     current_player = game_rules.current_turn
    #     opponent = 'white' if current_player == 'black' else 'black'

    #     # Check if the game is over first
    #     game_over = game_rules.is_game_over()
    #     if game_over:
    #         if "Checkmate" in game_over:
    #             status_display.update_status(game_over, "checkmate")
    #             sound_manager.play_checkmate_sound()
    #         elif "Stalemate" in game_over:
    #             status_display.update_status(game_over, "stalemate")
    #             sound_manager.play_move_sound()
    #         return True

    #     # Check for "Check" status
    #     if game_rules.is_in_check(current_player):
    #         checking_piece = None
    #         opponent_pieces = chess_board.get_pieces_by_color(opponent)
    #         king_position = chess_board.find_king(current_player).position

    #         for piece in opponent_pieces:
    #             if king_position in piece.get_possible_moves(chess_board):
    #                 checking_piece = f"{opponent.capitalize()}'s {piece.__class__.__name__}"
    #                 break

    #         status_display.update_status(
    #             f"{current_player.capitalize()} is in Check!",
    #             "check",
    #             checking_piece
    #         )
    #         sound_manager.play_check_sound()

    #     game_rules.switch_turn()
    #     sound_manager.play_move_sound()
    #     return True
    #  return False
    
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Handle AI turns
        current_turn = game_rules.current_turn
        current_ai = ai_white if current_turn == 'white' else ai_black

        if game_mode in ['Human_vs_AI', 'AI_vs_AI'] and current_ai:
            if not ai_move_ready.is_set():
                threading.Thread(target=calculate_ai_move, args=(current_ai, current_turn)).start()

            # Wait for AI move
            ai_move_ready.wait()
            with turn_lock:
                best_move = ai_move_results[current_turn]
                if best_move:
                    piece, new_position = best_move
                    handle_move(piece, new_position)
                    ai_move_ready.clear()
                    # pygame.time.wait(500)  # Add delay for visibility

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_mode == 'AI_vs_AI':
                    continue
                menu_action = game_menu.handle_click(mouse_pos)
                if menu_action:
                    if menu_action == 'resume':
                        game_menu.menu_open = False
                    elif menu_action == 'save_game':
                        save_game(chess_board, game_rules, game_mode)
                        print("Game saved successfully!")  # Debug message or feedback
                    elif menu_action == 'load_game':
                        success = load_game(chess_board, game_rules, game_mode)
                        if success:
                            print("Game loaded successfully!")
                        else:
                            print("Failed to load game!")
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
        status_display.draw_move_history(screen, game_rules.move_history)
        status_display.draw(screen)
        game_menu.draw_menu(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()