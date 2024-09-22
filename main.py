import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from floating_text import FloatingText
from state import State

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

    # Assign containers to classes for automatic group addition
    Asteroid.containers = (asteroid_group, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    FloatingText.containers = (all_text, updatable, drawable)
    State.containers = updatable

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

        score = state.player.get_score()
        play_time = state.player.get_time()

        if play_time >= 0 and play_time <= 0.1:
            # Clearing objects at respawning
            for text in all_text:
                text.kill()
            for i in asteroid_group:
                i.kill()     

        # Update all updatable sprites
        for sprite in updatable:
            sprite.update(dt)
        
        # Check for collisions if the player is alive
        if not state.player_dead:
            # Check for collisions between asteroids and the player
            for asteroid in asteroid_group:
                if asteroid.collision(state.player):
                    # Display collision messages
                    RGB = (250, 200, 100)
                    FloatingText(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 1, (f"Game Over!"), RGB, 4000)
                    FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 30), 1, (f"Your Score is {score}"), RGB, 4000)
                    FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 60), 1, (f"Yuo lasted {play_time} seconds"), RGB, 4000) 
                    FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 90), 1, (f"Press Return to play again"), RGB, 10000)
                    FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 120), 1, (f"Press ESC to quit"), RGB, 10000)                
                    # Remove the player and set game state
                    state.player.collide()
                    state.player_dead = True

        # Check for collisions between shots and asteroids
        for shot in shots:
            for asteroid in asteroid_group:
                if shot.collision(asteroid):
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
