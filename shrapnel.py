import pygame
import random
from circleshape import CircleShape
from floating_text import FloatingText

class Shrapnel(CircleShape):
    def __init__(self, x, y, radius, RGB=(235, 5, 2)):
        super().__init__(x, y, radius)
        self.lifetime = 700  # Lifetime in milliseconds
        self.spawn_time = pygame.time.get_ticks()
        self.rgb = RGB

    def draw(self, screen):
        # Draw the asteroid as a white circle
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
        flames = ["§", "¶", "∞", "∑", "≈", "Ω", "µ", "∆", "∫", "≈", "¬", "π", "≠", "√", "≤"]
        flame = random.choice(flames)
        FloatingText(self.position.x, self.position.y, 1, (f"{flame}"), self.rgb, 40)

    def update(self, dt):
        # Update position based on velocity and time delta
        self.position += self.velocity * dt
         # Remove the shrapnel if its lifetime has expired
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.kill()