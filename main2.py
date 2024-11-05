#Main2 File

import pygame
import sys
from chessboard import ChessBoard
from game_rules import GameRules
from sounds import SoundManager  # Import the SoundManager

pygame.init()
board_width, board_height = 600, 600
sidebar_width = 50  
screen_width = board_width + sidebar_width
screen = pygame.display.set_mode((screen_width, board_height))
pygame.display.set_caption('Chess Board')

chess_board = ChessBoard(screen, board_width, board_height)
game_rules = GameRules(chess_board)
sound_manager = SoundManager()  # Create an instance of SoundManager

clock = pygame.time.Clock()
running = True
selected_piece = None
dragging = False
initial_position = None

def draw_turn_indicator():
    sidebar_color = (0, 0, 0) if game_rules.current_turn == 'black' else (255, 255, 255)
    pygame.draw.rect(screen, sidebar_color, (board_width, 0, sidebar_width, board_height))

def draw_dragged_piece(piece, mouse_pos):
    offset_x = chess_board.tile_size // 2
    offset_y = chess_board.tile_size // 2
    x = mouse_pos[0] - offset_x
    y = mouse_pos[1] - offset_y
    screen.blit(piece.image, (x, y))

def handle_move(selected_piece, final_position):
    if chess_board.move_piece(selected_piece, final_position):
        if game_rules.is_in_check(game_rules.current_turn):
            selected_piece.position = initial_position  # Revert move
            return False
        sound_manager.play_move_sound()  # Play move sound
        game_rules.switch_turn()
        game_over = game_rules.is_game_over()
        if game_over:
            print(game_over)
            pygame.time.delay(2000)  # Pause to display the game-over message
            pygame.quit()
            sys.exit()
        return True
    else:
        selected_piece.position = initial_position  # Revert move
        return False

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            tile_position = chess_board.handle_click(position)
            piece = chess_board.get_piece_at(tile_position) if tile_position else None
            
            if piece and piece.color == game_rules.current_turn:
                selected_piece = piece
                initial_position = piece.position
                dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece and dragging:
                final_position = chess_board.handle_click(mouse_pos)
                if handle_move(selected_piece, final_position):
                    # Check for check or checkmate
                    if game_rules.is_in_check(game_rules.current_turn):
                        sound_manager.play_check_sound()
                    elif game_rules.is_checkmate(game_rules.current_turn):
                        sound_manager.play_checkmate_sound()

                selected_piece = None
                dragging = False
                initial_position = None

    screen.fill((255, 255, 255))
    chess_board.construct_board()

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

    for piece in chess_board.pieces:
        if piece != selected_piece or not dragging:
            piece.draw(chess_board.tile_size, chess_board.board_offset_x, chess_board.board_offset_y)
    
    if dragging and selected_piece:
        draw_dragged_piece(selected_piece, mouse_pos)

    draw_turn_indicator()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
