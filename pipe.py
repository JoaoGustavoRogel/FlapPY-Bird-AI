import pygame
from constants import *


class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/pipe-red.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, PIPE)

        self.rect = self.image.get_rect()
        self.rect[0] = x

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - y)
        else:
            self.rect[1] = SCREEN[1] - y

        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.rect[0] -= GAME_SPEED