"""
Class representing an Explosion in the game, which applies force to nearby objects based on proximity.

The Explosion has a radius that affects nearby objects within different distance thresholds (near, mid, far).
It can apply varying amounts of force depending on how close the object is to the center of the explosion.
Once the explosion occurs, it will be removed after applying the force.
"""

import pygame
from constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, multiplier=1):
        super().__init__(self.containers if hasattr(self, "containers") else None)  # Automatically add to sprite groups if defined
        self.is_explosion = True                                                  # Flag to identify explosion
        self.position = pygame.Vector2(x, y)                                      # Set explosion's position
        self.radius = EXPLOSION_INITIAL_RADIUS * multiplier                       # Explosion's radius for detection
        self.near = EXPLOSION_NEAR_RADIUS                                         # Close-range radius for high impact
        self.mid_radius = EXPLOSION_MID_RADIUS                                    # Mid-range radius for medium impact
        self.far_radius = EXPLOSION_FAR_RADIUS                                    # Far-range radius for low impact
        self.color = EXPLOSION_COLOR                                              # Explosion color for visual effects
        self.health = 1                                                           # Health for explosion (optional)

    def update(self, dt):
        pass                                                                      # No update logic for static explosion

    def collision(self, other, bounce=True):
        print(f"Explosion colliding with {other}")                                # Log explosion collision
        distance = self.position.distance_to(other.position)                      # Calculate distance to the other object
        
        if distance <= self.far_radius + other.radius:                            # Check if object is within far radius
            if distance <= self.near:                                             # Check if object is within close range
                strength = EXPLOSION_NEAR_STRENGTH                                # Apply near explosion strength
                self.calculate_force(other, strength)                             # Calculate and apply force
            elif distance <= self.mid_radius:                                     # Check if object is within mid range
                strength = EXPLOSION_MID_STRENGTH                                 # Apply mid explosion strength
                self.calculate_force(other, strength)                             # Calculate and apply force
            else:
                strength = EXPLOSION_FAR_STRENGTH                                 # Apply far explosion strength
                self.calculate_force(other, strength)                             # Calculate and apply force

    def calculate_force(self, other, strength):
        explosion_vector = other.position - self.position                         # Calculate direction of the force
        if explosion_vector.length() > 0:                                         # Normalize the vector if it has length
            explosion_vector.normalize_ip()                                       # Normalize in place
        force = explosion_vector * strength                                       # Calculate the force to be applied
        other.apply_force(force)                                                  # Apply the calculated force to the object
        self.kill()                                                               # Remove the explosion after applying force

    def draw(self, screen):
        for radius in [self.near, self.mid_radius, self.far_radius]:              # Draw concentric circles for explosion effect
            pygame.draw.circle(screen, self.color, 
                               (int(self.position.x + 1), int(self.position.y + 1)), 
                               int(radius), 2)                                    # Draw circle with explosion radii

    def apply_force(self, other):
        pass                                                                      # Placeholder for force application logic

    def shrapnel_obj(self, mass, RGB=(150, 150, 150)):
        pass                                                                      # Placeholder for shrapnel generation logic