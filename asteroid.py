import pygame                                  # Import the Pygame library for graphics
import random                                  # Import the random library for generating random values
from circle_shape import CircleShape            # Import the CircleShape base class for asteroid inheritance
from floating_text import FloatingText         # Import for displaying floating text in the game
from constants import *                        # Import game constants used for configuration

class Asteroid(CircleShape):
    """Class representing an asteroid that can split into smaller pieces or create shrapnel upon destruction."""

    def __init__(self, x, y, radius, RGB=(150, 150, 150), ):
        super().__init__(x, y, radius)             # Initialize base CircleShape with position and radius
        self.color = RGB                           # Set the color of the asteroid
        self.angular_velocity = 0                  # Disable angular velocity
        self.radius = radius                       # Set the asteroid's radius
        self.texture = generate_circular_texture(self.radius, self.color)  # Generate a texture based on the radius and color
        self.image = self.texture                  # Set the texture as the asteroid's image
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))  # Get rectangle around the image

    def update(self, dt):
        self.position += self.velocity * dt        # Update position based on velocity and delta time
        self.velocity *= self.friction             # Apply friction to gradually slow down movement
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))  # Update image rectangle position

    def shrapnel_obj(self, mass):
        """Asteroid's custom shrapnel generation, including splitting logic."""
        if self.destroyed:
            return
        self.kill()                                # Remove asteroid after being destroyed
        self.destroyed = True                      # Mark asteroid as destroyed to prevent further splitting
        if self.radius > ASTEROID_MIN_RADIUS:      # If asteroid is large enough, allow it to split
            self.split()                           # Call split method to create smaller asteroids
        else:
            self.create_shrapnel(mass)             # Otherwise, generate shrapnel instead of splitting

    def split(self):
        """Split the asteroid into two smaller pieces."""
        new_radius = self.radius / 2                                                                    # Reduce the radius by half for smaller asteroids
        offset_distance = new_radius * 2                                                                # Set distance to avoid overlapping smaller asteroids
        for i in range(2):                                                                              # Create two smaller asteroids
            angle_offset = 90 if i == 0 else -90                                                        # Separate the two smaller asteroids in opposite directions
            offset_direction = self.velocity.rotate(angle_offset).normalize()                           # Calculate the offset direction
            offset_position = self.position + offset_direction * offset_distance                        # New position for the smaller asteroid
            split_velocity = self.velocity.rotate(random.uniform(-30, 30)) * random.uniform(0.5, 1.5)   # Randomize velocity
            smaller_asteroid = Asteroid(offset_position.x, offset_position.y, new_radius, self.color)   # Create smaller asteroid
            smaller_asteroid.velocity = split_velocity                                                  # Assign velocity to the smaller asteroid
        self.create_shrapnel(15)                                                                        # Create shrapnel after splitting

    def draw(self, screen):
        """Draw the asteroid on the screen."""
        screen.blit(self.image, self.rect.topleft)                                  # Draw the asteroid image at the updated position

def generate_circular_texture(radius, base_color):
    """Generate a circular texture with noise for the asteroid."""
    texture_size = radius * 2                                                       # Texture size is based on diameter of the asteroid
    texture = pygame.Surface((texture_size, texture_size), pygame.SRCALPHA)         # Create a surface with transparency
    texture.fill((0, 0, 0, 0))                                                      # Fill the surface with a transparent background
    center = pygame.Vector2(radius, radius)                                         # Define the center of the texture
    pygame.draw.circle(texture, base_color, (int(center.x), int(center.y)), radius) # Draw the main circle for the asteroid

    for _ in range(1000):                                                           # Add random noise to the texture for a more natural look
        rand_x = random.randint(0, texture_size - 1)                                # Random X coordinate within the texture
        rand_y = random.randint(0, texture_size - 1)                                # Random Y coordinate within the texture
        distance = pygame.Vector2(rand_x, rand_y).distance_to(center)               # Calculate distance from the center
        if distance <= radius:                                                      # Only apply noise within the circular boundary
            brightness = random.randint(-50, 50)                                    # Random brightness variation
            random_color = (
                max(0, min(255, base_color[0] + brightness)),                       # Adjust red channel
                max(0, min(255, base_color[1] + brightness)),                       # Adjust green channel
                max(0, min(255, base_color[2] + brightness)),                       # Adjust blue channel
                255                                                                 # Keep fully opaque
            )
            texture.set_at((rand_x, rand_y), random_color)                          # Apply the random color to the texture
    return texture                                                                  # Return the generated texture for use
