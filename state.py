import pygame
from constants import *
from player import Player
from floating_text import FloatingText
class State():
    def __init__(self, player_dead):
        self.player_dead = player_dead
        self.player = None
        self.running = True

    def update(self, dt, updatable, drawable):
        # Draw time spent and score at the top of the screen
        score = self.player.get_score()
        RGB = (200, 200, 200)
        FloatingText(60, 20, 1, (f"Score is {score}"), RGB, 60)
        play_time = self.player.get_time()
        FloatingText(300, 20, 1, (f"Time played {play_time} s"), RGB, 60)

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
