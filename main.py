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

    # Assign containers to classes for automatic group addition
    Asteroid.containers = (asteroid_group, updatable, drawable, collidable_group)
    Player.containers = (updatable, drawable, collidable_group)
    Shot.containers = (shots, updatable, drawable, collidable_group)
    Shrapnel.containers = (updatable, drawable, collidable_group)
    AsteroidField.containers = updatable
    FloatingText.containers = (all_text, updatable, drawable)
    State.containers = (updatable, drawable)
    AlienShip.containers =(updatable, drawable, collidable_group, alien_ships) 

    # Initialize game state and player
    state = State(False)
    state.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,)
    updatable.add(state.player)
    drawable.add(state.player)
    asteroid_field = AsteroidField()
    alien_field = AlienField(state.player, asteroid_group)

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
            for i in alien_ships:
                i.kill()       
            state.new_game()

        # Optimise the game by killing items that go off screen
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        inflated_rect = screen_rect.inflate(10, 10)
        for item in collidable_group:
            if not inflated_rect.collidepoint(item.position):
                item.kill
                print(f"killing {item}")

        # Update all updatable sprites
        for sprite in updatable: 
            sprite.update(dt)        
        
        alien_field.update(dt, alien_ships)

        if state.player not in updatable:
            state.player_dead = True

        fps = round(clock.get_fps(), 2)
        all_objects = len(updatable)
        print(f"FPS: {fps}") 
        FloatingText(900, 20, (f"FPS: {fps} number of objects updatable: {all_objects} number of asteroids: {len(asteroid_group)}"), (255, 255, 255), 60)

        # Check for collisions between objects
        collidable_list = list(collidable_group)
        for i in range(len(collidable_list)):
            obj1 = collidable_list[i]
            for j in range(i + 1, len(collidable_list)):
                obj2 = collidable_list[j]
                obj1.collision(obj2)
                obj2.collision(obj1)
        
        def draw_health_bar(screen, x, y, current_health, max_health, bar_width=150, bar_height=10):
                health_percentage = current_health / max_health # Calculate health percentage
                health_width = bar_width * health_percentage
                pygame.draw.rect(screen, (200, 100, 100), (x, y, bar_width, bar_height))  # Red background
                pygame.draw.rect(screen, (100, 200, 100), (x, y, health_width, bar_height))  # Green health bar  
        draw_health_bar(screen, 500, 20, state.player.health, state.player.max_health)

        # Draw all drawable sprites
        for sprite in drawable:
            sprite.draw(screen)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()