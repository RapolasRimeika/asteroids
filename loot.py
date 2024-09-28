import pygame
import random
from asteroid import Asteroid
from floating_text import FloatingText
from constants import *

class LootSpawner(pygame.sprite.Sprite):
    containers = []
    
    def __init__(self, loot_parent, x, y, radius, delay):
        super().__init__(self.containers)  # Automatically add to all specified sprite groups
        self.loot_parent = loot_parent
        self.x = x
        self.y = y
        self.radius = radius
        self.delay = delay
        self.timer = 0
        self.loot_spawned = False
        self.position = pygame.Vector2(x, y)
        
    def update(self, dt):
        self.timer += dt
        # Check if delay has passed to spawn loot
        if self.timer >= self.delay and not self.loot_spawned:
            self.spawn_loot()

    def spawn_loot(self):
        new_loot = Loot(self.loot_parent, self.x, self.y, self.radius)
        self.loot_spawned = True  # Mark the loot as spawned

class Loot(Asteroid):
    # Define the types of loot with their effects and colors
    loot_types = {
        'health': {'color': LOOT_COLOR_HEALTH, 'effect': LOOT_EFFECT_HEAL, 'description': LOOT_DESCRIPTION_HEAL},
        'speed': {'color': LOOT_COLOR_SPEED, 'effect': LOOT_EFFECT_SPEED, 'description': LOOT_DESCRIPTION_SPEED},
        'score': {'color': LOOT_COLOR_SCORE, 'effect': LOOT_EFFECT_SCORE, 'description': LOOT_DESCRIPTION_SCORE},
        'fire': {'color': LOOT_COLOR_FIRE, 'effect': LOOT_EFFECT_FIRE, 'description': LOOT_DESCRIPTION_FIRE},
        'rotation': {'color': LOOT_COLOR_ROTATION, 'effect': LOOT_EFFECT_ROTATION, 'description': LOOT_DESCRIPTION_ROTATION},
        'stabilisers': {'color': LOOT_COLOR_STABILISERS, 'effect': LOOT_EFFECT_STABILISERS, 'description': LOOT_DESCRIPTION_STABILISERS},
        'dmg': {'color': LOOT_COLOR_DMG, 'effect': LOOT_EFFECT_DMG, 'description': LOOT_DESCRIPTION_DMG}
    }

    def __init__(self, loot_parent, x, y, radius):
        # Randomly choose a loot type from the defined types
        loot_type = random.choice(list(self.loot_types.keys()))
        
        # Set the color and effect of the loot based on its type
        loot_data = self.loot_types[loot_type]
        self.effect_type = loot_data['effect']
        self.loot_color = loot_data['color']
        self.description = loot_data['description']
        self.health = LOOT_HEALTH  # To ensure loot stays until picked up
        self.radius = radius
        self.is_loot = True

        # Initialize the loot object using the chosen color and parent class constructor
        super().__init__(x, y, radius, self.loot_color)

    def apply_effect(self, player):
        if self.effect_type == LOOT_EFFECT_HEAL:
            player.health += LOOT_HEAL_AMOUNT
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)
        
        elif self.effect_type == LOOT_EFFECT_SCORE:
            player.score_points(LOOT_SCORE_POINTS)
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)
        
        elif self.effect_type == LOOT_EFFECT_FIRE:
            player.shot_cooldown *= LOOT_FIRE_COOLDOWN_MULTIPLIER
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)
        
        elif self.effect_type == LOOT_EFFECT_DMG:
            player.shot_damage *= LOOT_DMG_MULTIPLIER
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)        
        
        elif self.effect_type == LOOT_EFFECT_SPEED:
            player.move_speed *= LOOT_SPEED_MULTIPLIER
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)

        elif self.effect_type == LOOT_EFFECT_ROTATION:
            player.turn_speed *= LOOT_ROTATION_MULTIPLIER
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)

        elif self.effect_type == LOOT_EFFECT_STABILISERS:
            if player.stabilisers == True:
                player.score_points(LOOT_ALREADY_HAVE_STABILISERS_POINTS)
                FloatingText(player.position.x, player.position.y, LOOT_ALREADY_HAVE_STABILISERS_MSG, self.loot_color, LOOT_MSG_DURATION)
            else:
                FloatingText(player.position.x, player.position.y, self.description, self.loot_color, LOOT_MSG_DURATION)

    def collision(self, other, bounce=True):
        # Check for collision with another object
        distance = self.position.distance_to(other.position)
        if (self.radius + LOOT_COLLECTION_BUFFER) + other.radius > distance:  # Use buffer for easy collection
            # If the object colliding with this loot is the player, apply the effect
            if hasattr(other, "is_player") and other.is_player == True:
                self.apply_effect(other)
                self.kill()  # Remove loot after applying the effect
