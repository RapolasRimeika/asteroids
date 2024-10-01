import pygame                                  # Pygame library for rendering and surface manipulation
import random                                  # Random library for generating random positions and velocities
from asteroid import Asteroid                  # Import the Asteroid class for spawning asteroids
from black_hole import BlackHole               # Import the BlackHole (BLK) class for black hole spawns
from constants import *                        # Import constants for screen dimensions and spawn rates

class AsteroidField(pygame.sprite.Sprite):
    """Class that handles the spawning of asteroids and black holes at the edges of the screen."""
    edges = [
        [pygame.Vector2(1, 0), lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)],                  # Left edge
        [pygame.Vector2(-1, 0), lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)],   # Right edge
        [pygame.Vector2(0, 1), lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS)],                   # Top edge
        [pygame.Vector2(0, -1), lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS)],   # Bottom edge
    ]

    def __init__(self,):
        pygame.sprite.Sprite.__init__(self, self.containers)  # Initialize sprite and containers
        self.spawn_timer = 0.0                               # Timer for spawning asteroids
        self.black_hole_timer = 0.0                          # Timer for spawning black holes
        self.black_hole_spawn_delay = 30.0                   # Delay between black hole spawns in seconds

    def spawn(self, radius, position, velocity):
        """Spawns a new asteroid at the given position with the specified velocity."""
        asteroid = Asteroid(position.x, position.y, radius)  # Create asteroid at given position
        asteroid.velocity = velocity                         # Set asteroid's velocity

    def spawn_black_hole(self):
        """Spawns a black hole at a random edge of the screen."""
        black_hole = BlackHole()                             # Create a new black hole instance
        edge = random.choice(self.edges)                     # Choose a random edge of the screen
        speed = random.randint(100, 150)                     # Set a random speed for the black hole
        velocity = edge[0] * speed                           # Calculate velocity based on edge direction
        velocity = velocity.rotate(random.randint(-30, 30))  # Add some randomness to the velocity
        position = edge[1](random.uniform(0, 1))             # Calculate a random position along the chosen edge
        black_hole.position = position                       # Set black hole position
        black_hole.velocity = velocity                       # Set black hole velocity

    def update(self, dt):
        """Updates the asteroid and black hole timers and spawns objects when needed."""
        self.spawn_timer += dt                               # Increment asteroid spawn timer
        if self.spawn_timer > ASTEROID_SPAWN_RATE:           # Check if it's time to spawn a new asteroid
            self.spawn_timer = 0                             # Reset spawn timer
            edge = random.choice(self.edges)                 # Choose a random edge
            speed = random.randint(200, 400)                 # Set random asteroid speed
            velocity = edge[0] * speed                       # Calculate asteroid velocity
            velocity = velocity.rotate(random.randint(-30, 30))  # Add some randomness to the velocity
            position = edge[1](random.uniform(0, 1))         # Set asteroid spawn position
            kind = random.randint(1, ASTEROID_KINDS)         # Randomly choose an asteroid kind
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)  # Spawn asteroid
        
        self.black_hole_timer += dt                          # Increment black hole spawn timer
        if self.black_hole_timer > self.black_hole_spawn_delay:  # Check if it's time to spawn a black hole
            self.spawn_black_hole()                          # Spawn black hole
            self.black_hole_timer = 0                        # Reset black hole spawn timer
