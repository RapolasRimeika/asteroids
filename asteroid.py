import pygame
import random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        # Initialize the asteroid with position and radius
        super().__init__(x, y, radius)
       
    def draw(self, screen):
        # Draw the asteroid as a white circle
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self, dt):
        # Update position based on velocity and time delta
        self.position += self.velocity * dt
        # Wrap around screen edges
        self.wrap_around_screen()

    def wrap_around_screen(self):
        # If the asteroid moves off-screen, wrap it to the opposite side
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def split(self):
        # Remove the current asteroid
        self.kill()
        # Stop splitting if the asteroid is at minimum size
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        # Create two smaller asteroids with new velocities
        random_angle = random.uniform(20, 50)
        velocity_a = self.velocity.rotate(random_angle) * 1.2
        velocity_b = self.velocity.rotate(-random_angle) * 1.2
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        # Spawn the new asteroids
        Asteroid(self.position.x, self.position.y, new_radius).velocity = velocity_a
        Asteroid(self.position.x, self.position.y, new_radius).velocity = velocity_b
