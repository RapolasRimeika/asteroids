import pygame
import random
from circleshape import CircleShape
from explosion import Explosion  # Import your Explosion class
from constants import *
from floating_text import FloatingText

class Shot(CircleShape):
    def __init__(self, x, y, radius, owner):
        super().__init__(x, y, radius)
        self.lifetime = 2000  # Lifetime in milliseconds
        self.spawn_time = pygame.time.get_ticks()
        self.owner = owner
        self.is_shot = True
        self.dt = 0
        # Disable angular velocity
        self.angular_velocity = 0

    def update(self, dt):
        # Update position based on velocity and time delta
        self.position += self.velocity * dt
        self.dt = dt
        # Apply linear friction to slow down movement over time
        self.velocity *= self.friction

        # Remove the shot if its lifetime has expired
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.kill()

    def collision(self, other, bounce=True):
        # Check for collision with another CircleShape
        bounce = False
        distance = self.position.distance_to(other.position)
        if (self.radius + 3) + other.radius > distance:
            self.shot_explode()


    def shot_explode(self):
        """ Method to handle the explosion of the shot """
        # Create the explosion object
        explosion = Explosion(self.position.x, self.position.y, 200)

        # Optionally, create shrapnel or other visual effects
        self.shrapnel_obj(self.radius, (150, 10, 15))

        # Destroy the shot after explosion
        self.kill()
