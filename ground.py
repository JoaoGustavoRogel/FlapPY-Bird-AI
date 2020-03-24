import pygame
from constants import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, width, height, x):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/base.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.scale(self.image, (width, height))
        
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = SCREEN[1] - height

    def update(self):
        self.rect[0] -= GAME_SPEED
