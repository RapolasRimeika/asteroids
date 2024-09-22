import pygame
import random
from constants import *
from player import Player
from floating_text import FloatingText

class State():
    def __init__(self, player_dead):
        self.player_dead = player_dead
        self.player = None
        self.running = True
        self.score = 0
        self.play_time = 0

    def update(self, dt, updatable, drawable):
                
        # update time spent and score at the top of the screen
        self.score = self.player.get_score()
        self.play_time = self.player.get_time()
        #draw
        RGB = (200, 200, 200)
        FloatingText(60, 20, 1, (f"Score is {self.score}"), RGB, 60)
        FloatingText(300, 20, 1, (f"Time played {self.play_time} s"), RGB, 60)

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

    def player_death(self):
        # Draw death summary
        RGB = (250, 200, 100)
        FloatingText(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 1, (f"Game Over!"), RGB, 4000)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 30), 1, (f"Your Score is {self.score}"), RGB, 4000)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 60), 1, (f"Yuo lasted {self.play_time} seconds"), RGB, 4000) 
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 90), 1, (f"Press Return to play again"), RGB, 10000)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 120), 1, (f"Press ESC to quit"), RGB, 10000)

    def new_game(self):
        # New game message
            start_messages = ["Ready to rock... literally!", "Let's smash some rocks!", "Asteroids beware, here we come!", "Get your space boots on, it's go time!", "Time to turn asteroids into dust!", "Prepare for asteroid annihilation!", "Space rocks don't stand a chance!", "Strap in, it's gonna be a rocky ride!", "Break some cosmic stuff!", "Warning: Asteroids about to get wrecked!", "Engage asteroid-smashing mode!", "Ready, aim, asteroid!", "Asteroids... meet your doom!", "Suit up, space warrior!", "Send those asteroids packing!"]
            start_message = random.choice(start_messages)
            RGB = (250, 200, 100)
            FloatingText(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 100, 1, (f"{start_message}"), RGB, 4000)