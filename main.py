import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from floating_text import FloatingText
from state import State
from circleshape import Shrapnel
from aliens import AlienShip
from AlienField import AlienField
from loot import Loot, LootSpawner
from explosion import Explosion
from blk import BLK
from background_layers import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    all_text = pygame.sprite.Group()
    shrapnel_group = pygame.sprite.Group()
    collidable_group = pygame.sprite.Group()
    alien_ships = pygame.sprite.Group()
    loot_group = pygame.sprite.Group()
    loot_spawner_group = pygame.sprite.Group() 
    all_explosions = pygame.sprite.Group()
    clearable_group = pygame.sprite.Group()

    # Assign containers to classes for automatic group addition
    Player.containers = (updatable, drawable, collidable_group)
    AsteroidField.containers = (updatable)
    LootSpawner.containers = (updatable, loot_spawner_group)
    Asteroid.containers = (asteroid_group, updatable, drawable, collidable_group, clearable_group)
    Shot.containers = (shots, updatable, drawable, collidable_group, clearable_group)
    Shrapnel.containers = (updatable, drawable, collidable_group, clearable_group)
    FloatingText.containers = (all_text, updatable, drawable, clearable_group)
    AlienShip.containers =(updatable, drawable, collidable_group, alien_ships, clearable_group) 
    Loot.containers = (loot_group, updatable, drawable, collidable_group, clearable_group)
    Explosion.containers = (updatable, drawable, all_text, collidable_group, clearable_group)
    BLK.containers = (updatable, drawable, collidable_group, clearable_group) 

    # Initialize game state, spawn flields, player, background
    state = State(False)
    state.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,)
    alien_field = AlienField(state.player, asteroid_group)
    asteroid_field = AsteroidField()
    drawable.add(state.player)
    updatable.add(state.player, alien_field, asteroid_field)
        
    state.running = True    
    while state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.blit(state.background, (0, 0))             # wipe the screen with the generated background
        state.draw(screen)   
        dt = clock.tick(60) / 1000                  # Cap the frame rate at 60 FPS and calculate delta time
        state.update(dt, updatable, drawable, collidable_group, clearable_group)# Update the game state        
        for sprite in updatable:                                                # Update all updatable sprites
            sprite.update(dt)

        collidable_list = list(collidable_group)                                # Check for collisions between objects
        for i in range(len(collidable_list)):
            obj1 = collidable_list[i]
            for j in range(i + 1, len(collidable_list)):
                obj2 = collidable_list[j]
                obj1.collision(obj2)
                obj2.collision(obj1)
        
        #DEBUGGING stuff
        """fps = round(clock.get_fps(),)
        all_objects = len(updatable)
        print(f"FPS: {fps}") 
        FloatingText(900, 20, (f"FPS: {fps} number of objects updatable: {all_objects} number of asteroids: {len(asteroid_group)}"), (255, 255, 255), 60)"""
        for sprite in drawable:                                                 # Draw all drawable sprites
            sprite.draw(screen)
        state.draw(screen)          
        pygame.display.flip()                                                    # Update the display

if __name__ == "__main__":
    main()