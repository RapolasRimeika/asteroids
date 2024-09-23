import pygame
from circleshape import CircleShape
from constants import *
from floating_text import FloatingText

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        # Initialize the shot with position and radius
        super().__init__(x, y, radius)
        self.lifetime = 2000  # Lifetime in milliseconds
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Draw the shot as a small circle
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
        RGB = (255, 0, 0)
        FloatingText(self.position.x, self.position.y, ".", RGB, 40)

    def update(self, dt):
        # Update position based on velocity and time delta
        self.position += self.velocity * dt
        # Remove the shot if its lifetime has expired
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.kill()

    def collision(self, other, bounce=False):
        distance = self.position.distance_to(other.position)
        if self.radius + other.radius > distance:
            other.health -= self.radius * self.speed
             # Call the explosion method
            self.shot_explode(other)
            # Kill the shot after the explosion
            self.kill()
            return True
        return False

    def shot_explode(self, other):
        """ Method to handle the explosion of the shot, creating shrapnel """
        self.shrapnel_obj(self.radius)  # Create shrapnel pieces when the shot explodes
        other.health - PLAYER_SHOT_DMG          
