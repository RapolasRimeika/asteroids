import pygame
import random
from circleshape import CircleShape
from floating_text import FloatingText

class Shrapnel(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.lifetime = 2000  # Lifetime in milliseconds
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Draw the asteroid as a white circle
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
        RGB = (255, 0, 0)
        flames = ["§", "¶", "∞", "∑", "≈", "Ω", "µ", "∆", "∫", "≈", "¬", "π", "≠", "√", "≤"]
        flame = random.choice(flames)
        FloatingText(self.position.x, self.position.y, 1, (f"{flame}"), RGB, 40)

    def update(self, dt):
        # Update position based on velocity and time delta
        self.position += self.velocity * dt
         # Remove the shrapnel if its lifetime has expired
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.kill()