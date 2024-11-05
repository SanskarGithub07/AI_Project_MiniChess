import pygame
import sys
from chessboard import ChessBoard

pygame.init()
board_width, board_height = 800, 600
sidebar_width = 50  
screen_width = board_width + sidebar_width
screen = pygame.display.set_mode((screen_width, board_height))
pygame.display.set_caption('Chess Board')

chess_board = ChessBoard(screen, board_width, board_height)

clock = pygame.time.Clock()
running = True
selected_piece = None
dragging = False
initial_position = None
current_turn = 'white'
game_state = 'ongoing'  # 'ongoing', 'checkmate', 'stalemate'

def draw_turn_indicator():
    sidebar_color = (0, 0, 0) if current_turn == 'black' else (255, 255, 255)
    pygame.draw.rect(screen, sidebar_color, (board_width, 0, sidebar_width, board_height))

def draw_dragged_piece(piece, mouse_pos):
    # Calculate center offset
    offset_x = chess_board.tile_size // 2
    offset_y = chess_board.tile_size // 2
    
    # Draw piece centered on mouse
    x = mouse_pos[0] - offset_x
    y = mouse_pos[1] - offset_y
    screen.blit(piece.image, (x, y))

def draw_game_state_text():
    font = pygame.font.Font(None, 36)
    if game_state == 'checkmate':
        text = font.render("Checkmate! {} wins.".format('Black' if current_turn == 'white' else 'White'), True, (255, 0, 0))
    elif game_state == 'stalemate':
        text = font.render("Stalemate!", True, (255, 0, 0))
    elif chess_board.is_in_check(current_turn):
        text = font.render("{} is in check.".format(current_turn.capitalize()), True, (255, 0, 0))
    else:
        return
    
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

screen_height = board_height

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            tile_position = chess_board.handle_click(position)
            piece = chess_board.get_piece_at(tile_position) if tile_position else None
            
            if piece and piece.color == current_turn:
                selected_piece = piece
                initial_position = piece.position
                dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece and dragging:
                final_position = chess_board.handle_click(mouse_pos)
                if final_position and chess_board.move_piece(selected_piece, final_position):
                    # Check for check, checkmate, and stalemate
                    if current_turn == 'white' and chess_board.is_checkmate('white'):
                        game_state = 'checkmate'
                        running = False
                    elif current_turn == 'black' and chess_board.is_checkmate('black'):
                        game_state = 'checkmate'
                        running = False
                    elif current_turn == 'white' and chess_board.is_stalemate('white'):
                        game_state = 'stalemate'
                        running = False
                    elif current_turn == 'black' and chess_board.is_stalemate('black'):
                        game_state = 'stalemate'
                        running = False
                    else:
                        current_turn = 'black' if current_turn == 'white' else 'white'
                else:
                    # If move is invalid, return piece to initial position
                    selected_piece.position = initial_position
                    
                selected_piece = None
                dragging = False
                initial_position = None

    # Draw the board and pieces
    screen.fill((255, 255, 255))
    chess_board.construct_board()

    # Draw possible moves if piece is selected
    if selected_piece:
        # Highlight original position
        x = chess_board.board_offset_x + initial_position[1] * chess_board.tile_size
        y = chess_board.board_offset_y + initial_position[0] * chess_board.tile_size
        pygame.draw.rect(screen, (255, 255, 0), (x, y, chess_board.tile_size, chess_board.tile_size), 3)

        # Show possible moves
        for move in selected_piece.get_possible_moves(chess_board):
            move_x = chess_board.board_offset_x + move[1] * chess_board.tile_size
            move_y = chess_board.board_offset_y + move[0] * chess_board.tile_size
            highlight_surface = pygame.Surface((chess_board.tile_size, chess_board.tile_size), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, (0, 255, 0, 128), highlight_surface.get_rect())
            screen.blit(highlight_surface, (move_x, move_y))
    
    # Draw all pieces except the dragged one
    for piece in chess_board.pieces:
        if piece != selected_piece or not dragging:
            piece.draw(chess_board.tile_size, chess_board.board_offset_x, chess_board.board_offset_y)
    
    # Draw the dragged piece last (on top) if dragging
    if dragging and selected_piece:
        draw_dragged_piece(selected_piece, mouse_pos)

    draw_turn_indicator()
    draw_game_state_text()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()