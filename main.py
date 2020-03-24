import pygame
import random
from bird import Bird
from pipe import Pipe
from constants import *
from ground import Ground
from pygame.locals import *


def init():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN)

    return screen

def is_out_screen(sprite):
    return sprite.rect[0] < -sprite.rect[2]

def get_random_pipes(x):
    size = random.randint(100, 300)

    pipe = Pipe(False, x, size)
    pipe_inv = Pipe(True, x, SCREEN[1] - size - PIPE_GAP)

    return (pipe, pipe_inv)

if __name__ == "__main__":
    screen = init()

    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)
    
    ground_group = pygame.sprite.Group()
    ground_group.add(Ground(2 * SCREEN[0], 100, 0))
    ground_group.add(Ground(2 * SCREEN[0], 100, 2*SCREEN[0]))

    pipe_group = pygame.sprite.Group()
    pipe_group.add(get_random_pipes(600)[0])
    pipe_group.add(get_random_pipes(600)[1])
    pipe_group.add(get_random_pipes(600 + SCREEN[0])[0])
    pipe_group.add(get_random_pipes(600 + SCREEN[0])[1])

    clock = pygame.time.Clock()

    while 42:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird.bump()
        screen.blit(BACKGROUND, (0, 0))

        if is_out_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(2 * SCREEN[0], 100, 2 * SCREEN[0] - 20)
            ground_group.add(new_ground)

        if is_out_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            pipes = get_random_pipes(SCREEN[0] * 2)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        
        bird_group.update()
        ground_group.update()
        pipe_group.update()

        pipe_group.draw(screen)
        ground_group.draw(screen)
        bird_group.draw(screen)
        

        if pygame.sprite.groupcollide(bird_group, ground_group, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(bird_group, pipe_group, False, pygame.sprite.collide_mask):
            break

        pygame.display.update()
        