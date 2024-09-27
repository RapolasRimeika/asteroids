import pygame
import random
from circleshape import CircleShape
from floating_text import FloatingText
from constants import *
from text_lists import explosion_list

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, RGB=(150, 150, 150), ):

        super().__init__(x, y, radius)
        self.color = RGB
        self.angular_velocity = 0 # Disable angular velocity
        self.radius = radius
        self.texture = generate_circular_texture(self.radius, self.color)
        self.image = self.texture
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))

    def update(self, dt):
        self.position += self.velocity * dt # Update position based on velocity and time delta
        self.velocity *= self.friction # Apply linear friction to slow down movement over time
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))        
        # When the asteroid's health drops, split
        if self.health <= (self.max_health / 3) and self.radius > ASTEROID_MIN_RADIUS:
            self.split()
        elif self.health <= 0:
            # If the asteroid is at its smallest size and health is depleted, produce shrapnel
            self.shrapnel_obj(self.radius)
            self.kill()

    def split(self):
            self.kill()
            # Split the asteroid into two smaller pieces
            new_radius = self.radius / 2
            # Define an offset distance to ensure the new asteroids do not overlap
            offset_distance = new_radius * 2.8
            for i in range(2):          # Create two smaller asteroids
                # Calculate the direction of the offset (opposite for each asteroid)
                angle_offset = 90 if i == 0 else -90  # Separate asteroids in opposite directions
                offset_direction = self.velocity.rotate(angle_offset).normalize()           
                offset_position = self.position + offset_direction * offset_distance # Apply the offset to the position
                # Create the smaller asteroid at the new offset position
                split_velocity = self.velocity.rotate(random.uniform(-30, 30)) * random.uniform(0.5, 1.5)
                smaller_asteroid = Asteroid(offset_position.x, offset_position.y, new_radius, self.color)
                smaller_asteroid.velocity = split_velocity
            self.shrapnel_obj(10, self.color)            # Create shrapnel

    def draw(self, screen):
        # update the texture rectangle position and blit it 
        screen.blit(self.image, self.rect.topleft)

def generate_circular_texture(radius, base_color):
    # Create a square surface with dimensions of (diameter x diameter)
    texture_size = radius * 2
    texture = pygame.Surface((texture_size, texture_size), pygame.SRCALPHA)  # Use SRCALPHA for transparency

    # Fill the surface with transparent color (for non-circular areas)
    texture.fill((0, 0, 0, 0))  # Transparent background (RGBA)

    # Draw a circular shape with the base color and random noise
    for _ in range(500):  # Adjust the number of random noise dots
        # Generate random positions within the circular boundary
        rand_x = random.randint(0, texture_size - 1)
        rand_y = random.randint(0, texture_size - 1)
        # Calculate distance from the center to ensure we are inside the circle
        center = pygame.Vector2(radius, radius)
        distance = pygame.Vector2(rand_x, rand_y).distance_to(center)
        if distance <= radius:
            brightness = random.randint(-50, 50) # Vary the brightness of the base color for texture
            random_color = (
                max(0, min(255, base_color[0] + brightness)),
                max(0, min(255, base_color[1] + brightness)),
                max(0, min(255, base_color[2] + brightness)),
                255  # Fully opaque
                )
            texture.set_at((rand_x, rand_y), random_color)
    return texture