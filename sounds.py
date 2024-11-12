import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound("sounds/move.wav")
        self.check_sound = pygame.mixer.Sound("sounds/check.wav")
        self.checkmate_sound = pygame.mixer.Sound("sounds/checkmate.wav")

    def play_move_sound(self):
        self.move_sound.play()

    def play_check_sound(self):
        self.check_sound.play()

    def play_checkmate_sound(self):
        self.checkmate_sound.play()
