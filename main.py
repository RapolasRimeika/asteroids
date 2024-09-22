import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from floating_text import FloatingText
from state import State
from shrapnel import Shrapnel

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

    # Assign containers to classes for automatic group addition
    Asteroid.containers = (asteroid_group, updatable, drawable, collidable_group)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable, collidable_group)
    Shot.containers = (shots, updatable, drawable, collidable_group)
    Shrapnel.containers = (updatable, drawable, collidable_group)
    FloatingText.containers = (all_text, updatable, drawable)
    State.containers = (updatable, drawable)
    

    # Initialize game state and player
    state = State(False)
    state.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    updatable.add(state.player)
    drawable.add(state.player)
    asteroid_field = AsteroidField()

    state.running = True    
    while state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Clear the screen
        screen.fill((15, 15, 0))
        # Cap the frame rate at 60 FPS and calculate delta time
        dt = clock.tick(60) / 1000

        # Update the game state
        state.update(dt, updatable, drawable)
        # Clearing objects at respawning
        if state.player.time >= 0 and state.player.time <= 0.005:
            for text in all_text:
                text.kill()
            for i in asteroid_group:
                i.kill()   
            state.new_game()  
        # Optimise the game by killing items that go off screen
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        inflated_rect = screen_rect.inflate(60, 60)
        for item in collidable_group:
            if not inflated_rect.collidepoint(item.position):
                item.kill


        # Update all updatable sprites
        for sprite in updatable:
            sprite.update(dt)
        
       
        # Check for collisions between objects
        collidable_list = list(collidable_group)
        for i in range(len(collidable_list)):
            obj1 = collidable_list[i]
            for j in range(i + 1, len(collidable_list)):
                obj2 = collidable_list[j]
                obj1.collision(obj2)
                
       # if asteroid.collision(state.player, bounce=False):
            # Remove the player and set game state
        #        state.player.collide()
         #       state.player_collision()
          #      state.player_dead = True

        # Check for collisions between shots and asteroids
        for shot in shots:
            for asteroid in asteroid_group:
                if shot.collision(asteroid, bounce=False):
                    asteroid.split()
                    state.player.score_points(1)
                    state.player.destroy_asteroid(1)
                    shot.kill()
                    break  # Move to the next shot


        # Draw all drawable sprites
        for sprite in drawable:
            sprite.draw(screen)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
