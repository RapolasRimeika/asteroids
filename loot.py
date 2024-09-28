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
        'health': {'color': (0, 255, 0), 'effect': 'heal', 'description': '+200 Health'},
        'speed': {'color': (0, 0, 255), 'effect': 'speed', 'description': 'Engine upgrade!'},
        'score': {'color': (255, 255, 0), 'effect': 'score', 'description': '+50 Score'},
        'fire': {'color': (255, 0, 255), 'effect': 'fire', 'description': 'Fire rate increase!'},
        'rotation': {'color': (0, 50, 200), 'effect': 'rotation', 'description': 'Thruster upgrade!'},
        'stabilisers': {'color': (99, 50, 15), 'effect': 'stabilisers', 'description': 'STABILISERS!!!!'},
        'dmg': {'color': (255, 0, 75), 'effect': 'dmg', 'description': 'Fire damage increase!'} 
    }

    def __init__(self, loot_parent, x, y, radius):
        # Randomly choose a loot type from the defined types
        loot_type = random.choice(list(self.loot_types.keys()))
        
        # Set the color and effect of the loot based on its type
        loot_data = self.loot_types[loot_type]
        self.effect_type = loot_data['effect']
        self.loot_color = loot_data['color']
        self.description = loot_data['description']
        self.health = 1000000000  # To ensure loot stays until picked up
        self.radius = radius
        self.is_loot = True

        # Initialize the loot object using the chosen color and parent class constructor
        super().__init__(x, y, radius, self.loot_color)

    def apply_effect(self, player):
       
        if self.effect_type == 'heal':
            heal_amount = 200  # Heal up to 20 points
            player.health += heal_amount
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, 1000)
        
        elif self.effect_type == 'score':
            player.score_points(50)  # Add 50 points to the player's score
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, 1000)
        
        elif self.effect_type == 'fire':
            player.shot_cooldown *= 0.7 #faster shooting rate
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, 1000)
        
        elif self.effect_type == 'dmg':
            player.shot_damage *= 2 # increased damage
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, 1000)        
        
        elif self.effect_type == 'speed':
            player.move_speed *= 1.2  # engine upgrade
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, 1000)

        elif self.effect_type == 'rotation':
            player.turn_speed *= 1.2 #faster turning speed
            FloatingText(player.position.x, player.position.y, self.description, self.loot_color, 1000)

        elif self.effect_type == 'stabilisers':
            if player.stabilisers == True:
                 #faster shooting rate
                player.score_points(50)  # Add 50 points to the player's score
                FloatingText(player.position.x, player.position.y, "Already have Stabilisers, let's sell it", self.loot_color, 1000)
            else:
                FloatingText(player.position.x, player.position.y, self.description, self.loot_color, 1000)


    def collision(self, other, bounce=True):
        # Check for collision with another object
        distance = self.position.distance_to(other.position)
        if (self.radius + 5) + other.radius > distance: # +5 for easy collection
            # If the object colliding with this loot is the player, apply the effect
            if hasattr(other, "is_player") and other.is_player == True:
                self.apply_effect(other)
                self.kill()  # Remove loot after applying the effect
            
