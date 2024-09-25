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
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    chess_board.construct_board()
    chess_board.draw_pieces()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
