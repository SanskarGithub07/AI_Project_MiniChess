import pygame
import sys
from chessboard import ChessBoard

pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess Board')

chess_board = ChessBoard(screen, width, height)

clock = pygame.time.Clock()
running = True
selected_piece = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            tile_position = chess_board.handle_click(position)
            piece = chess_board.get_piece_at(tile_position)
            if piece:
                selected_piece = piece
                initial_position = tile_position
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece:
                final_position = chess_board.handle_click(pygame.mouse.get_pos())
                chess_board.move_piece(selected_piece, final_position)
                selected_piece = None
        elif event.type == pygame.MOUSEMOTION:
            if selected_piece:
                new_position = chess_board.handle_click(pygame.mouse.get_pos())
                chess_board.move_piece(selected_piece, new_position)
      
	# everything below is outside of movement event loop and runs under while
    screen.fill((255, 255, 255))
    chess_board.construct_board()
    chess_board.draw_pieces()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
