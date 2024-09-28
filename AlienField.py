import pygame
import random
from aliens import AlienShip
from constants import *

class AlienField(pygame.sprite.Sprite):
    """ Manages the spawning and timing of alien ships in the game.

    The `AlienField` class is responsible for periodically spawning alien ships at random positions
    along the edges of the screen. Each alien ship targets the player and avoids asteroids. The class
    maintains a reference to the player and the asteroid objects to ensure proper interaction between
    the aliens and other game elements.

    Attributes:
        player (Player): A reference to the player object, used to determine the target of alien ships.
        asteroids (list): A reference to the list of asteroids in the game to avoid during alien movement.
        spawn_timer (float): A timer that tracks when to spawn the next alien ship, reset after each spawn.
    
    Methods:
        spawn(): Creates a new alien ship at a random position along the screen edges and returns it.
        update(dt): Updates the spawn timer and spawns a new alien ship when the timer exceeds the set spawn rate."""
    
    def __init__(self, player, asteroids):
        pygame.sprite.Sprite.__init__(self)
        self.player = player        # Reference to the player object
        self.asteroids = asteroids  # Reference to the asteroid list
        self.spawn_timer = 0.0      # Timer to control spawn intervals

    def spawn(self): # Choose a random spawn position along the screen edges
        edges = [
            pygame.Vector2(0, random.uniform(0, SCREEN_HEIGHT)),            # Left
            pygame.Vector2(SCREEN_WIDTH, random.uniform(0, SCREEN_HEIGHT)), # Right
            pygame.Vector2(random.uniform(0, SCREEN_WIDTH), 0),             # Top
            pygame.Vector2(random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT)  # Bottom
        ]
        position = random.choice(edges)
        alien_ship = AlienShip(position.x, position.y, ALIEN_RADIUS, self.player, self.asteroids,) # Create an alien ship
        return alien_ship

    def update(self, dt):
        self.spawn_timer += dt                      # Update the spawn timer
        if self.spawn_timer > ALIEN_SPAWN_RATE:     # Check if it's time to spawn a new alien
            self.spawn_timer = 0
            alien = self.spawn()

