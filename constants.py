import pygame
from pygame.locals import *

SCREEN = (300, 600)
INITIAL_SPEED = 100
GAME_SPEED = 10
SPEED = 10
GRAVITY = 1
BACKGROUND = pygame.transform.scale(pygame.image.load('images/background-day.png'), SCREEN)
PIPE = (75, 500)
PIPE_GAP = 150