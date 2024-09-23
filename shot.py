import pygame
from circleshape import CircleShape
from circleshape import Shrapnel
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

    def collision(self, other, bounce=True):
        distance = self.position.distance_to(other.position)
        if self.radius + other.radius > distance:
            self.health -= other.radius * other.speed
            self.shot_explode(other)
                    
    def shot_explode(self, other):
         other.health - PLAYER_SHOT_DMG
         self.shrapnel_obj(self.radius)
