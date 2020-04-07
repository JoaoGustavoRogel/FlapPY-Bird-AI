import pygame
from constants import *

class Bird(pygame.sprite.Sprite):
    def __init__(self, random_x, random_y, color, initial_x = 150):
        pygame.sprite.Sprite.__init__(self)

        self.random_x = random_x
        self.random_y = random_y

        self.speed = SPEED

        self.images = [
            pygame.image.load(f"images/{color}-bird-upflap.png").convert_alpha(),
            pygame.image.load(f"images/{color}-bird-midflap.png").convert_alpha(),
            pygame.image.load(f"images/{color}-bird-downflap.png").convert_alpha()
        ]

        self.current_image = 0
        
        self.image = pygame.image.load(f"images/{color}-bird-midflap.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = (SCREEN[0] / 2) - initial_x
        self.rect[1] = SCREEN[1] / 2


    def update(self):
        self.current_image += 1
        self.current_image %= 3
        self.image = self.images[self.current_image]

        self.speed += 1

        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def calc_distance(self, target_x, target_y):
        return (target_x, target_y)

    def neuronio(self, x, y):
        calc = (self.random_x * x) + (self.random_y * y)

        if calc > 0:
            self.bump()
