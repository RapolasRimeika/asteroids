import pygame
import random
from asteroid import Asteroid
from blk import BLK  # Import the BLK class
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    # Edges of the screen for spawning objects
    edges = [
        # Left edge
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        # Right edge
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        # Top edge
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        # Bottom edge
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
        ],
    ]

    def __init__(self,):
        # Initialize sprite and set the spawn timers
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.black_hole_timer = 0.0         # Timer for black holes
        self.black_hole_spawn_delay = 30.0   # Time delay between black hole spawns (in seconds)


    def spawn(self, radius, position, velocity):
        # Create a new asteroid with specified parameters
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def spawn_black_hole(self):
        # Create a new black hole with specified parameters
        black_hole = BLK()
        # Spawn at a random edge
        edge = random.choice(self.edges)
        speed = random.randint(100, 150)
        velocity = edge[0] * speed
        velocity = velocity.rotate(random.randint(-30, 30))
        position = edge[1](random.uniform(0, 1))
        black_hole.position = position
        black_hole.velocity = velocity

    def update(self, dt):
        # Update the asteroid spawn timer
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0
            # Spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(200, 400)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
        
    # Handle black hole spawning logic
        self.black_hole_timer += dt
        if self.black_hole_timer > self.black_hole_spawn_delay:
            self.spawn_black_hole()
            self.black_hole_timer = 0  # Reset the timer after spawning a black hole