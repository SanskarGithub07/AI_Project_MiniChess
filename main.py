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
<<<<<<< Updated upstream
            
            if selected_piece is None:
                piece = chess_board.get_piece_at(tile_position)
                if piece:
                    selected_piece = piece
            else:
                if chess_board.move_piece(selected_piece, tile_position):
                    selected_piece = None
                else:
                    selected_piece = None

=======
            if piece:
                selected_piece = piece
                # indicates that this piece is ready to move
            elif selected_piece:
            	# attempts to move the selected piece to the clicked tile position
                chess_board.move_piece(selected_piece, tile_position)
                # reset the selection so nothing is selected
                selected_piece = None
                
	# everything below is outside of the event loop and runs under while
>>>>>>> Stashed changes
    screen.fill((255, 255, 255))
    chess_board.construct_board()
    if selected_piece:
        chess_board.draw_possible_moves(selected_piece)
    chess_board.draw_pieces()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
