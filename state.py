import pygame
import random
from constants import *
from player import Player
from floating_text import FloatingText
from text_lists import start_messages

class State():
    def __init__(self, player_dead):
        self.player_dead = player_dead
        self.player = None
        self.running = True
        self.score = 0
        self.play_time = 0
        self.high_score = 0  # Initialize high score

    def update(self, dt, updatable, drawable):
                
        # update time spent and score at the top of the screen
        self.score = self.player.get_score()
        self.play_time = self.player.get_time()
        #draw
        RGB = (200, 200, 200)
        FloatingText(70, 20, (f"Score is {self.score}"), RGB, 3)
        FloatingText(300, 20, (f"Time played {self.play_time} s"), RGB, 3)
        
        # Check for player respawn
        keys = pygame.key.get_pressed()
        if self.player_dead and keys[pygame.K_RETURN]:
            # Player is dead and Enter key is pressed
            # Create a new player instance
            self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.player_dead = False

        if self.player_dead:
            self.player_death()

        if keys[pygame.K_ESCAPE]:
            self.running = False

        if self.score > self.high_score:
            self.high_score = self.score

    def player_death(self):
        # Draw death summary
        RGB = (250, 200, 100)
        FloatingText(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, (f"Game Over!"), RGB, 4)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 40), (f"Your Score is {self.score}"), RGB, 4)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 80), (f"Yuo lasted {self.play_time} seconds"), RGB, 4) 
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 120), (f"High Score: {self.high_score}"), RGB, 4)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 160), (f"Press Return to play again"), RGB, 4)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 200), (f"Press ESC to quit"), RGB, 4)
        
    def new_game(self):
            start_message = random.choice(start_messages)
            RGB = (250, 200, 100)
            FloatingText(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 100, (f"{start_message}"), RGB, 4000)

          