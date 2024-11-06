import pygame
import sys
from chessboard import ChessBoard
from game_rules import GameRules
from sounds import SoundManager

# Initialize pygame and sound manager
pygame.init()
sound_manager = SoundManager()

# Screen setup
board_width, board_height = 600, 600
sidebar_width = 50  
screen_width = board_width + sidebar_width
screen = pygame.display.set_mode((screen_width, board_height))
pygame.display.set_caption('Chess Board')

# Initialize game components
chess_board = ChessBoard(screen, board_width, board_height)
game_rules = GameRules(chess_board)


# Set up the clock for controlling the frame rate and running loop control
clock = pygame.time.Clock()
running = True
selected_piece = None
dragging = False
initial_position = None

# Initialize font
font = pygame.font.SysFont("Arial", 24, bold=True)

def draw_turn_indicator():
    sidebar_color = (0, 0, 0) if game_rules.current_turn == 'black' else (255, 255, 255)
    pygame.draw.rect(screen, sidebar_color, (board_width, 0, sidebar_width, board_height))

def draw_dragged_piece(piece, mouse_pos):
    """
    Draws the piece being dragged at the current mouse position.
    Offsets the piece image so it follows the mouse accurately.
    """
    offset_x = chess_board.tile_size // 2
    offset_y = chess_board.tile_size // 2
    x = mouse_pos[0] - offset_x
    y = mouse_pos[1] - offset_y
    screen.blit(piece.image, (x, y))

def draw_game_status():
    """Display check, checkmate, or stalemate messages on the screen."""
    status_message = ""
    if game_rules.is_in_check(game_rules.current_turn):
        status_message = f"{game_rules.current_turn.capitalize()} is in Check!"
    game_over = game_rules.is_game_over()
    if game_over:
        status_message = game_over

    if status_message:
        text_surface = font.render(status_message, True, (255, 0, 0))  # Red text for emphasis
        screen.blit(text_surface, (10, 10))  # Position at top-left corner

def handle_move(selected_piece, final_position):
    """
    Attempts to move the selected piece to the final position.
    Checks if the move is legal and plays appropriate sounds based on game state.
    Returns True if the move is valid, otherwise False.
    """
    if game_rules.is_move_legal(selected_piece, final_position) and chess_board.move_piece(selected_piece, final_position):
        if game_rules.is_in_check(game_rules.current_turn):
            print(f"{game_rules.current_turn.capitalize()} is in check.")
            sound_manager.play_check_sound()  # Play check sound

        game_over = game_rules.is_game_over()
        if game_over:
            print(game_over)
            # Play the checkmate sound for checkmate; otherwise, a regular move sound
            if "Checkmate" in game_over:
                sound_manager.play_checkmate_sound()
            elif "Stalemate" in game_over:
                sound_manager.play_move_sound()  # Stalemate as a regular move sound
            else:
                sound_manager.play_move_sound()

            pygame.time.delay(2000)  # Pause to display the game-over message
            pygame.quit()
            sys.exit()

        else:
            sound_manager.play_move_sound()  # Regular move sound if no game-ending state
        game_rules.switch_turn()
        return True
    else:
        selected_piece.position = initial_position  # Revert move if invalid
        return False

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #end game
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #handle oiece selection
            position = pygame.mouse.get_pos()
            tile_position = chess_board.handle_click(position)
            piece = chess_board.get_piece_at(tile_position) if tile_position else None
            
            if piece and piece.color == game_rules.current_turn:
                selected_piece = piece
                initial_position = piece.position
                dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            # Handle piece drop and attempt to finalize move
            if selected_piece and dragging:
                final_position = chess_board.handle_click(mouse_pos)
                handle_move(selected_piece, final_position)
                selected_piece = None
                dragging = False
                initial_position = None

    #clear screen for redraw
    screen.fill((255, 255, 255))
    chess_board.construct_board()

    #highlight possible moves for selected piece
    if selected_piece:
        x = chess_board.board_offset_x + initial_position[1] * chess_board.tile_size
        y = chess_board.board_offset_y + initial_position[0] * chess_board.tile_size
        pygame.draw.rect(screen, (255, 255, 0), (x, y, chess_board.tile_size, chess_board.tile_size), 3)

        possible_moves = selected_piece.get_possible_moves(chess_board)
        for move in possible_moves:
            move_x = chess_board.board_offset_x + move[1] * chess_board.tile_size
            move_y = chess_board.board_offset_y + move[0] * chess_board.tile_size
            highlight_surface = pygame.Surface((chess_board.tile_size, chess_board.tile_size), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, (0, 255, 0, 128), highlight_surface.get_rect())
            screen.blit(highlight_surface, (move_x, move_y))

    # Draw all pieces except the one currently being dragged
    for piece in chess_board.pieces:
        if piece != selected_piece or not dragging:
            piece.draw(chess_board.tile_size, chess_board.board_offset_x, chess_board.board_offset_y)
    
    # Draw the piece being dragged following the mouse cursor
    if dragging and selected_piece:
        draw_dragged_piece(selected_piece, mouse_pos)

    # Draw the turn indicator in the sidebar
    draw_turn_indicator()
    draw_game_status()  # Draw the game status message on the board
    pygame.display.flip()
    clock.tick(60)

#exit the game
pygame.quit()
sys.exit()
