import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

# creating groups    
    updatable = pygame.sprite.Group() 
    drawable = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()

    Asteroid.containers = (asteroid_group, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)

# creating instances
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    dt = 0

    running = True    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))
        dt = clock.tick(60) / 1000
        for i in updatable:
            i.update(dt)
            print(f"updating {i}")

        for i in drawable:
            i.draw(screen)
            print(f"drawing object:{i}")
        
        pygame.display.flip()


if __name__ == "__main__":
    main()
