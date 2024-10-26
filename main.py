import pygame
import sys
from chessboard import ChessBoard

pygame.init()
board_width, board_height = 600, 600
sidebar_width = 50  
screen_width = board_width + sidebar_width
screen = pygame.display.set_mode((screen_width, board_height))
pygame.display.set_caption('Chess Board')

chess_board = ChessBoard(screen, board_width, board_height)

clock = pygame.time.Clock()
running = True
selected_piece = None
current_turn = 'white'

def draw_turn_indicator():
    sidebar_color = (0, 0, 0) if current_turn == 'black' else (255, 255, 255)
    pygame.draw.rect(screen, sidebar_color, (board_width, 0, sidebar_width, board_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            tile_position = chess_board.handle_click(position)
            piece = chess_board.get_piece_at(tile_position)
            if selected_piece is None:
                piece = chess_board.get_piece_at(tile_position)
                if piece and piece.color == current_turn:
                    selected_piece = piece
            else:
                if chess_board.move_piece(selected_piece, tile_position):
                    current_turn = 'black' if current_turn == 'white' else 'white'
                selected_piece = None

    screen.fill((255, 255, 255)) 
    chess_board.construct_board()  

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

    chess_board.draw_pieces() 
    draw_turn_indicator()  

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
