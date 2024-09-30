import pygame
import random
from constants import *
from player import Player
from floating_text import FloatingText
from text_lists import start_messages
from asteroidfield import AsteroidField
from background import generate_star_and_planet_background

class State():
    """
    Manages the game state, including player status, score, health, and background generation.

    The `State` class is responsible for tracking the player's state (alive or dead), updating the game,
    handling respawns, drawing the health bar and death summary, and managing the score and high score.

    Attributes:
        background (Surface): The star and planet background generated for the game.
        player_dead (bool): Indicates if the player is currently dead.
        player (Player): The player object, initialized when the game starts or respawns.
        running (bool): Flag indicating if the game is currently running.
        play_time (float): The total playtime in seconds.
        high_score (int): The highest score achieved during the game.
        score (int): The current player's score.
        health (int): The current player's health.
    """

    def __init__(self, player_dead):
        self.background = generate_star_and_planet_background(SCREEN_WIDTH, SCREEN_HEIGHT, 1000, 3, (50, 100))  # Generate the background
        self.player_dead = player_dead        # Initial player death state
        self.player = None                    # Player is not initialized at the start
        self.running = True                   # The game starts in a running state
        self.play_time = 0                    # Initialize playtime to 0
        self.high_score = 0                   # Initialize high score
        self.score = 0                        # Initialize score
        self.health = 0                       # Initialize health

    def update(self, dt, updatable, drawable, collidable_group, clearable_group):
        keys = pygame.key.get_pressed()         # Get current key presses
        if keys[pygame.K_ESCAPE]:               # Exit the game if ESC is pressed
            self.running = False
        if self.player.score > self.high_score: # Update high score if the player's score exceeds it
            self.high_score = self.player.score
        if self.player not in updatable:        # Check if the player is dead
            self.player_death()
            self.player_dead = True

        if self.player_dead and keys[pygame.K_RETURN]:   # Respawn player when Enter is pressed
            self.player_respawn(keys, clearable_group)
        self.cull_offscreen_objects(collidable_group)   # Call the culling function
        self.update_player_stats()                      # Call the player stats update function

    def player_respawn(self, keys, clearable_group):
        """
        Respawns the player when Enter is pressed, resets the background, and clears relevant game objects.

        Args:
            keys (list): The current state of keyboard inputs.
            clearable_group (pygame.sprite.Group): Group of objects to be cleared upon player respawn.
        """
        if self.player_dead and keys[pygame.K_RETURN]:  # Respawn player when Enter is pressed
            self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)           # Create a new player
            self.background = generate_star_and_planet_background(SCREEN_WIDTH, SCREEN_HEIGHT, 1000, 3, (50, 100))  # Generate a new background
            self.player_dead = False                                             # Set player_dead flag to False
            for i in clearable_group:
                i.kill()                                                         # Remove objects in clearable_group
            self.new_game()                                                      # Start a new game

    def update_player_stats(self):
        """
        Updates the player's score, playtime, and health.
        """
        self.score = self.player.score               # Update the player's score
        self.play_time = round(self.player.time)     # Update playtime in seconds
        self.health = self.player.health             # Update the player's health


    def draw(self, screen):
        pygame.draw.rect(screen, (100, 200, 100), (1250, 1250, self.health, 10))  # Draw the green health bar
        FloatingText(175, 20, (f"Score is {self.score}  Time played {self.play_time} s"), TEXT_COLOR, 10)  # Display score and time


    def cull_offscreen_objects(self, collidable_group):
        """
        Removes objects that are off-screen by a certain margin.
        """
        off_screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)    # Define the screen boundaries
        inflated_rect = off_screen_rect.inflate(125, 125)                   # Expand the boundary for off-screen items
        for item in collidable_group:                                       # Loop through collidable items
            if not inflated_rect.collidepoint(item.position):               # Remove items outside the boundary
                item.kill()                                                 # Remove the object from the game


    def player_death(self):
        """
        Displays the player's death summary when they die.
        """
        death_summary = (
            f"Game Over!\n"
            f"Your Score is {self.player.score}\n"
            f"You lasted {round(self.player.time)} seconds\n"
            f"High Score: {self.high_score}\n"
            f"Press Return to play again\n"
            f"Press ESC to quit")
        FloatingText(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, death_summary, TEXT_COLOR, 10)  # Display the death summary

    def new_game(self):
        """
        Starts a new game with a random start message.
        """
        start_message = random.choice(start_messages)  # Select a random start message
        FloatingText(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 100, (f"{start_message}"), TEXT_COLOR, 4000)  # Display the start message
