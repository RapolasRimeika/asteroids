import pygame
from constants import *
from player import Player

class State():
    def __init__(self, player_dead):
        self.player_dead = player_dead
        self.player = None
        self.running = True

    def update(self, dt, updatable, drawable):
        # Check for player respawn
        keys = pygame.key.get_pressed()
        if self.player_dead and keys[pygame.K_RETURN]:
            # Player is dead and Enter key is pressed
            # Create a new player instance
            self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            updatable.add(self.player)
            drawable.add(self.player)
            self.player_dead = False
        
        if keys[pygame.K_ESCAPE]:
            self.running = False
