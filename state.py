import pygame
import random
from constants import *
from player import Player
from floating_text import FloatingText
from text_lists import start_messages
from asteroidfield import AsteroidField
from background_layers import generate_star_and_planet_background

class State():
    def __init__(self, player_dead):
        self.player_dead = player_dead
        self.player = None
        self.running = True
        self.play_time = 0
        self.high_score = 0  # Initialize high score
        self.score = 0
        self.health = 0
        self.background = generate_star_and_planet_background(SCREEN_WIDTH, SCREEN_HEIGHT, 1000, 3, (50, 100))

    def update(self, dt, updatable, drawable, collidable_group, clearable_group):    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:   self.running = False
        if self.player.score > self.high_score:   self.high_score = self.player.score        
        if self.player not in updatable:                                    # Check player alive
            self.player_death()
            self.player_dead = True
        if self.player_dead and keys[pygame.K_RETURN]:                      # Player is dead and Enter key is pressed
            self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)       # Create a new player instance
            self.background = generate_star_and_planet_background(SCREEN_WIDTH, SCREEN_HEIGHT, 1000, 3, (50, 100))
 
            self.player_dead = False
        if self.player.time >= 0 and self.player.time <= 0.005:             # Clearing objects at respawning
            for i in clearable_group: i.kill()
            self.new_game()

        off_screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)    # Optimise the game by killing items that go off screen
        inflated_rect = off_screen_rect.inflate(150, 150)                   # Inflate the screen rectangle by amount of pixels on each side
        for item in collidable_group:                                       # Loop through each item in the collidable_group
            if not inflated_rect.collidepoint(item.position):               # Check if the item's position is outside the inflated screen area
                item.kill()

        self.score = self.player.score
        self.play_time = round(self.player.time)
        self.health = self.player.health
        RGB = (200, 200, 200)
        FloatingText(70, 20, (f"Score is {self.score}"), RGB, 10)
        FloatingText(300, 20, (f"Time played {self.play_time} s"), RGB, 10)

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 200, 100), (1250, 1250, self.health, 10))     # Green health bar
        

    def player_death(self): # Draw death summary
        RGB = (250, 200, 100)
        FloatingText(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,           (f"Game Over!"), RGB, 10)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 40),   (f"Your Score is {self.player.score}"), RGB, 10)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 80),   (f"Yuo lasted {round(self.player.time)} seconds"), RGB, 10) 
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 120),  (f"High Score: {self.high_score}"), RGB, 10)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 160),  (f"Press Return to play again"), RGB, 10)
        FloatingText(SCREEN_WIDTH / 2, ((SCREEN_HEIGHT / 2)+ 200),  (f"Press ESC to quit"), RGB, 10)
        
    def new_game(self):
        start_message = random.choice(start_messages)
        RGB = (250, 200, 100)
        FloatingText(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 100, (f"{start_message}"), RGB, 4000)

