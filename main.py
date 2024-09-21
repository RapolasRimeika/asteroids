import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from floating_text import FloatingText

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

# creating groups    
    updatable = pygame.sprite.Group() 
    drawable = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    all_text = pygame.sprite.Group()

    Asteroid.containers = (asteroid_group, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    FloatingText.containers = (all_text, updatable, drawable)

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
        
        for i in asteroid_group:
            if i.collision(player):
                print("Game Over!")
                return 
            for shot in shots:
                if shot.collision(i):
                    i.split()
                    RGB = (255, 0, 150)
                    new_message = FloatingText(i.position[0], i.position[1], 1,"POW!", RGB, 500)

        for i in drawable:
            i.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
