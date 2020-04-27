import neat
import time
import pygame
import random
import threading
from bird import Bird
from pipe import Pipe
from constants import *
from ground import Ground
from pygame.locals import *
from problem import Problem


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

def generate_inital_population(size):
    birds = []
    color = 1
    for _ in range(size):
        birds.append(Bird(random.randint(-5, 5), random.randint(-5, 5), color, random.randint(50, 150)))
        color %= 3
        color += 1

    return birds

def eval_genomes(genomes, config):
    nets = []
    bird_group = pygame.sprite.Group()
    birds = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(random.randint(1, 3)))
        ge.append(genome)

    
    ground_group = pygame.sprite.Group()
    ground_group.add(Ground(2 * SCREEN[0], 100, 0))
    ground_group.add(Ground(2 * SCREEN[0], 100, 2*SCREEN[0]))

    pipe_group = pygame.sprite.Group()
    pipe_group.add(get_random_pipes(600)[0])
    pipe_group.add(get_random_pipes(600)[1])
    pipe_group.add(get_random_pipes(600 + SCREEN[0])[0])
    pipe_group.add(get_random_pipes(600 + SCREEN[0])[1])

    clock = pygame.time.Clock()

    bird_life = True
    while bird_life and len(birds) > 0:
        clock.tick(25)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

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

        for i, bird in enumerate(birds):
            ge[i].fitness += 0.1
            by = bird.rect[1]
            py = pipe_group.sprites()[0].rect[1]

            output = nets[birds.index(bird)].activate((by, abs(by - py), abs(by - py + PIPE_GAP)))
            if output[0] > 0.5:
                bird.bump()
            
        bird_group = pygame.sprite.Group()
        for bird in birds:
            bird_group.add(bird)

        cont_died = 0
        for bird in birds:
            flag = True
            if bird.is_collided_with(pipe_group.sprites()[0]) or bird.is_collided_with(pipe_group.sprites()[1]) or bird.is_collided_with(ground_group.sprites()[0]):
                bird.die()
                ge[birds.index(bird)].fitness -= 1
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))
                flag = False

            if flag and (bird.rect[1] > ground_group.sprites()[0].rect[1] or bird.rect[1] > SCREEN[1]):
                bird.die()
                bird.die()
                ge[birds.index(bird)].fitness -= 1
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

            if not bird.is_life:
                cont_died += 1
      
        bird_group.update()
        ground_group.update()
        pipe_group.update()

        pipe_group.draw(screen)
        ground_group.draw(screen)
        bird_group.draw(screen)
        
        
        if cont_died == len(bird_group):
            bird_life = False

        pygame.display.update()

def play_song():
    pygame.mixer.music.load('songs/main_song.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(1)

    clock = pygame.time.Clock()
    clock.tick(10)

    while pygame.mixer.music.get_busy():
        print("Tocando música")
        pygame.event.poll()
        clock.tick(10)

def run():
    config_file = "config.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    p = neat.Population(config)
    
    t = threading.Thread(target=play_song)
    t.start()

    p.run(eval_genomes, 100)


if __name__ == "__main__":
    screen = init()

    run()
        