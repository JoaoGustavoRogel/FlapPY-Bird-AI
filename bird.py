import pygame
from constants import *

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = SPEED

        self.images = [
            pygame.image.load("images/bluebird-upflap.png").convert_alpha(),
            pygame.image.load("images/bluebird-midflap.png").convert_alpha(),
            pygame.image.load("images/bluebird-downflap.png").convert_alpha()
        ]

        self.current_image = 0
        
        self.image = pygame.image.load("images/bluebird-midflap.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN[0] / 2
        self.rect[1] = SCREEN[1] / 2


    def update(self):
        self.current_image += 1
        self.current_image %= 3
        self.image = self.images[self.current_image]

        self.speed += 1

        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED
