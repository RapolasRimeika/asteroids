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
    """
    The main function initializes the Pygame environment, creates game entities and sprite groups,
    and runs the game loop. It handles events, updates the game state, checks for collisions, and
    renders all game elements on the screen. The game loop continues until the player exits the game.

    Sprite groups include updatable, drawable, collidable, and clearable objects such as the player,
    asteroids, alien ships, shots, and various effects like explosions and floating text.
    """

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
            
    state.running = True                                        # Set game state to running
    while state.running:                                        # Game loop runs while state is active
        for event in pygame.event.get():                        # Process all game events
            if event.type == pygame.QUIT:                       # Check if the quit event is triggered
                return                                          # Exit the game loop if quit is triggered
        screen.blit(state.background, (0, 0))                   # Wipe the screen with the generated background
        state.draw(screen)                                      # Draw the game state on the screen
        dt = clock.tick(60) / 1000                              # Cap the frame rate at 60 FPS and calculate delta time
        state.update(dt, updatable, drawable, collidable_group, clearable_group) # Update game state, passing groups for updating
        for sprite in updatable:                                # Update all sprites marked as updatable
            sprite.update(dt)                                   # Call the update method for each sprite with delta time
        collidable_list = list(collidable_group)                # Create a list of collidable objects
        for i in range(len(collidable_list)):                   # Loop through each collidable object
            obj1 = collidable_list[i]                           # First object in the collision pair
            for j in range(i + 1, len(collidable_list)):        # Loop through the remaining objects to check for collisions
                obj2 = collidable_list[j]                       # Second object in the collision pair
                obj1.collision(obj2)                            # Check for a collision between obj1 and obj2
                obj2.collision(obj1)                            # Check for a collision between obj2 and obj1 (reverse order)
        for sprite in drawable:                                 # Loop through all drawable sprites
            sprite.draw(screen)                                 # Draw each sprite on the screen
        state.draw(screen)                                      # Draw the game state elements on the screen
        pygame.display.flip()                                   # Update the display with all the new drawings

if __name__ == "__main__":                                      # If this script is run as the main program
    main()                                                      # Call the main function to start the game