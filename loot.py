import pygame                                         # Pygame library for game development
import random                                         # Random library to choose loot types randomly
from asteroid import Asteroid                         # Import the Asteroid class for loot inheritance
from floating_text import FloatingText                # Import for displaying text messages on the screen
from constants import *                               # Import all constants used for game configuration

class LootSpawner(pygame.sprite.Sprite):              # Class for spawning loot items after delay
    containers = []                                   # Container groups to add this object into
    def __init__(self, loot_parent, x, y, radius, delay):
        super().__init__(self.containers)             # Add the spawner to the specified sprite groups
        self.loot_parent = loot_parent                # Parent object that spawns the loot
        self.x = x                                    # X position for loot spawning
        self.y = y                                    # Y position for loot spawning
        self.radius = radius                          # Radius of the loot object
        self.delay = delay                            # Delay before spawning loot
        self.timer = 0                                # Timer for tracking the delay
        self.loot_spawned = False                     # Track if loot has been spawned
        self.position = pygame.Vector2(x, y)          # Position vector for spawning the loot
        
    def update(self, dt):                             # Method to update the spawner each frame
        self.timer += dt                              # Increment the timer based on the delta time
        if self.timer >= self.delay and not self.loot_spawned:  # Check if delay passed and loot not spawned
            self.spawn_loot()                         # Call the method to spawn loot

    def spawn_loot(self):                             # Method to spawn the loot object
        new_loot = Loot(self.loot_parent, self.x, self.y, self.radius)  # Create new loot at given position
        self.loot_spawned = True                      # Mark loot as spawned to prevent re-spawning

class Loot(Asteroid):                                 # Loot class inherits from Asteroid
    loot_types = {                                    # Define types of loot with effects and colors
        'health': {'color': LOOT_COLOR_HEALTH, 'effect': LOOT_EFFECT_HEAL, 'description': LOOT_DESCRIPTION_HEAL},
        'speed': {'color': LOOT_COLOR_SPEED, 'effect': LOOT_EFFECT_SPEED, 'description': LOOT_DESCRIPTION_SPEED},
        'score': {'color': LOOT_COLOR_SCORE, 'effect': LOOT_EFFECT_SCORE, 'description': LOOT_DESCRIPTION_SCORE},
        'fire': {'color': LOOT_COLOR_FIRE, 'effect': LOOT_EFFECT_FIRE, 'description': LOOT_DESCRIPTION_FIRE},
        'rotation': {'color': LOOT_COLOR_ROTATION, 'effect': LOOT_EFFECT_ROTATION, 'description': LOOT_DESCRIPTION_ROTATION},
        'stabilisers': {'color': LOOT_COLOR_STABILISERS, 'effect': LOOT_EFFECT_STABILISERS, 'description': LOOT_DESCRIPTION_STABILISERS},
        'dmg': {'color': LOOT_COLOR_DMG, 'effect': LOOT_EFFECT_DMG, 'description': LOOT_DESCRIPTION_DMG}
    }

    def __init__(self, loot_parent, x, y, radius):
        loot_type = random.choice(list(self.loot_types.keys()))   # Choose a random loot type
        loot_data = self.loot_types[loot_type]                    # Get data for the selected loot type
        self.effect_type = loot_data['effect']                    # Set the effect type for this loot
        self.loot_color = loot_data['color']                      # Set the color for this loot
        self.description = loot_data['description']               # Set the description for this loot
        self.health = LOOT_HEALTH                                 # Set health so loot can stay until picked
        self.radius = radius                                      # Set the radius of the loot object
        self.is_loot = True                                       # Mark object as loot for collision checks
        super().__init__(x, y, radius, self.loot_color)           # Call parent class (Asteroid) constructor with loot color

    def apply_effect(self, player):                               # Apply the loot effect to the player
        if self.effect_type == LOOT_EFFECT_HEAL:                  # If the effect is healing
            player.health += LOOT_HEAL_AMOUNT                     # Increase player health
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)  # Display text

        elif self.effect_type == LOOT_EFFECT_SCORE:               # If the effect is increasing score
            player.score_points(LOOT_SCORE_POINTS)                # Add points to player's score
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)  # Display text

        elif self.effect_type == LOOT_EFFECT_FIRE:                # If the effect is decreasing fire cooldown
            player.shot_cooldown *= LOOT_FIRE_COOLDOWN_MULTIPLIER # Reduce player's cooldown between shots
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)  # Display text

        elif self.effect_type == LOOT_EFFECT_DMG:                 # If the effect is increasing damage
            player.shot_damage *= LOOT_DMG_MULTIPLIER             # Increase player's shot damage
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)  # Display text

        elif self.effect_type == LOOT_EFFECT_SPEED:               # If the effect is increasing speed
            player.move_speed *= LOOT_SPEED_MULTIPLIER            # Increase player's movement speed
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)  # Display text

        elif self.effect_type == LOOT_EFFECT_ROTATION:            # If the effect is increasing rotation speed
            player.turn_speed *= LOOT_ROTATION_MULTIPLIER         # Increase player's turning speed
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)  # Display text

        elif self.effect_type == LOOT_EFFECT_STABILISERS:         # If the effect is increasing stabiliser strength
            player.stabiliser_str *= 1.2                          # Increase player's stabiliser strength by 20%
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)  # Display text

    def collision(self, other, bounce=True):                      # Check for collision with another object
        distance = self.position.distance_to(other.position)      # Calculate the distance between this object and the other
        if (self.radius + LOOT_COLLECTION_BUFFER) + other.radius > distance:  # If within collection range
            if hasattr(other, "is_player") and other.is_player == True:       # Check if the other object is the player
                self.apply_effect(other)                         # Apply the loot effect to the player
                self.kill()                                      # Remove the loot after applying the effect
