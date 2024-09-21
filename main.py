import pygame
from chessboard import ChessBoard

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

chess_board = ChessBoard(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((255, 255, 255))
    
    chess_board.construct_board()
    
            
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
    