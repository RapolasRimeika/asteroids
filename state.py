import pygame
import random
import json
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
        state (str): The current state of the game ('PLAYING', 'GAME_OVER', 'NAME_ENTRY', 'RESPAWN_WAIT').
        high_scores (list): List of high score entries loaded from file.
        player_name (str): The name entered by the player upon game over.
        floating_texts (pygame.sprite.Group): Group of floating text sprites to display.
    """

    def __init__(self, player_dead):
        self.background = generate_star_and_planet_background(SCREEN_WIDTH, SCREEN_HEIGHT, 1000, 3, (50, 100))
        self.player_dead = player_dead        # Initial player death state
        self.player = None                    # Player is not initialized at the start
        self.running = True                   # The game starts in a running state
        self.play_time = 0                    # Initialize playtime to 0
        self.high_score = 0                   # Initialize high score
        self.score = 0                        # Initialize score
        self.health = 0                       # Initialize health
        self.high_scores = load_high_scores() # Load high scores from file
        self.player_name = ""                 # Empty player name to input upon death
        self.name_entered = False             # Flag to indicate if the name has been entered
        self.state = 'PLAYING'                # Possible states: 'PLAYING', 'GAME_OVER', 'NAME_ENTRY', 'RESPAWN_WAIT'
        self.floating_texts = pygame.sprite.Group()  # Group to manage floating text sprites
        self.new_game()  # Start a new game

    def update(self, dt, updatable, drawable, collidable_group, clearable_group, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
                self.running = False

        if self.state == 'PLAYING':
            # Update player stats
            self.update_player_stats()

            # Check if the player has died
            if self.player not in updatable:
                self.state = 'GAME_OVER'

        elif self.state == 'GAME_OVER':
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = 'NAME_ENTRY'

        elif self.state == 'NAME_ENTRY':
            self.input_player_name(events)
            if self.name_entered:
                self.save_score()
                self.state = 'RESPAWN_WAIT'

        elif self.state == 'RESPAWN_WAIT':
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.player_respawn(clearable_group)
                    self.state = 'PLAYING'

        # Update floating texts
        self.floating_texts.update(dt)

        # Cull offscreen objects
        self.cull_offscreen_objects(collidable_group)

    def update_player_stats(self):
        """Updates the player's score, playtime, and health."""
        if self.player:
            self.score = self.player.score               # Update the player's score
            self.play_time = round(self.player.time)     # Update playtime in seconds
            self.health = self.player.health             # Update the player's health

    def draw(self, screen):
        if self.state == 'PLAYING':
            self.draw_stats(screen)
            # Draw floating texts
            for floating_text in self.floating_texts:
                floating_text.draw(screen)
        elif self.state == 'GAME_OVER':
            # Draw game over screen
            self.draw_game_over(screen)
        elif self.state == 'NAME_ENTRY':
            # Draw name entry screen
            self.draw_name_entry(screen)
        elif self.state == 'RESPAWN_WAIT':
            # Draw respawn prompt
            self.draw_respawn_prompt(screen)

            # Always draw floating texts
            self.floating_texts.draw(screen)

    def draw_stats(self, screen):
        # --- Draw Health Bar ---
        # Set the width of the health bar
        max_health_width = 200
        health_ratio = self.health / 100  # Assuming health is out of 100
        health_bar_width = max(0, max_health_width * health_ratio)  # Ensure health bar width is non-negative

        # Move health bar slightly up from the bottom (increase gap)
        health_bar_y_position = SCREEN_HEIGHT - 100  # Adjust Y position of the health bar

        # Draw the health bar in the bottom center
        pygame.draw.rect(screen, (100, 0, 0), 
                        (SCREEN_WIDTH / 2, health_bar_y_position, max_health_width, 10))  # Background
        pygame.draw.rect(screen, (0, 250, 0), 
                        (SCREEN_WIDTH / 2, health_bar_y_position, health_bar_width, 10))  # Health bar

        # --- Draw Score and Time ---
        font = pygame.font.SysFont(None, FONT_SIZE)

        # Prepare the text with score and time
        score_time_text = f"Score: {self.score} | Time: {self.play_time}s"
        score_time_surface = font.render(score_time_text, True, TEXT_COLOR)

        # Draw the score and time with more padding from the edges
        padding = 40
        screen.blit(score_time_surface, (SCREEN_WIDTH - score_time_surface.get_width() - padding, padding))

    def cull_offscreen_objects(self, collidable_group):
        """
        Removes objects that are off-screen by a certain margin.
        """
        off_screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        inflated_rect = off_screen_rect.inflate(125, 125)
        for item in collidable_group:
            if not inflated_rect.collidepoint(item.position):
                item.kill()

    def input_player_name(self, events):
        """Handles player name input after death."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.player_name:
                        self.name_entered = True
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    if len(self.player_name) < 10 and event.unicode.isprintable():
                        self.player_name += event.unicode.upper()

    def save_score(self):
        """Saves the player's score and sorts the high score list."""
        new_entry = {'name': self.player_name, 'score': self.score, 'time': self.play_time}
        self.high_scores.append(new_entry)
        self.high_scores = sorted(self.high_scores, key=lambda x: -x['score'])[:10]  # Keep top 10
        save_high_scores(self.high_scores)

    def player_respawn(self, clearable_group):
        """Respawns the player, resets the background, and clears relevant game objects."""
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.background = generate_star_and_planet_background(SCREEN_WIDTH, SCREEN_HEIGHT, 1000, 3, (50, 100))
        self.name_entered = False
        self.player_name = ""
        for obj in clearable_group:
            obj.kill()
        self.new_game()

    def new_game(self):
        """Starts a new game with a random start message."""
        start_message = random.choice(start_messages)
        start_text = FloatingText(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100, start_message, TEXT_COLOR, 4000)
        self.floating_texts.add(start_text)

    def draw_game_over(self, screen):
        """Draws the game over screen with instructions."""
        # Display game over message
        lines = [
            "Game Over!",
            f"Your Score: {self.score}",
            f"Time Played: {self.play_time}s",
            "Press Return to enter your name"
        ]
        self.display_multiline_text(screen, lines, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)
        self.display_high_scores_on_screen(screen)

    def draw_name_entry(self, screen):
        """Draws the name entry screen with instructions."""
        # Display name entry prompt
        lines = [
            "Enter your name (max 10 characters):",
            self.player_name,
            "Press Return when done"
        ]
        self.display_multiline_text(screen, lines, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)

    def draw_respawn_prompt(self, screen):
        """Draws the respawn prompt screen with instructions."""
        lines = [
            "Press Return to respawn and start a new game"
        ]
        self.display_multiline_text(screen, lines, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def display_multiline_text(self, screen, lines, x, y):
        """Helper method to display multiple lines of text."""
        font = pygame.font.Font(None, FONT_SIZE)
        line_height = font.get_linesize()
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, TEXT_COLOR)
            rect = text_surface.get_rect(center=(x, y + i * line_height))
            screen.blit(text_surface, rect)

    def display_high_scores_on_screen(self, screen):
        """Displays the high scores on the screen."""
        font = pygame.font.Font(None, FONT_SIZE)
        line_height = font.get_linesize()
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2 + 50
        title_surface = font.render("High Scores:", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(x, y))
        screen.blit(title_surface, title_rect)
        y += line_height * 1.5

        # Iterate through the high score entries
        for entry in self.high_scores:
            # Only display if the entry has a valid name
            if len(entry['name']) >= 1:
                line = f"{entry['name']} - {entry['score']} pts, {entry['time']}s"
                text_surface = font.render(line, True, TEXT_COLOR)
                rect = text_surface.get_rect(center=(x, y))
                screen.blit(text_surface, rect)
                y += line_height

def load_high_scores():
    """Load high scores from a file or create a default one if not found."""
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default high score list with 0 scores and times
        return [{'name': '', 'score': 0, 'time': 0} for _ in range(10)]

def save_high_scores(high_scores):
    """Save the updated high scores to a file."""
    try:
        with open(HIGH_SCORE_FILE, 'w') as file:
            json.dump(high_scores, file)
    except IOError as e:
        print(f"Error saving high scores: {e}")