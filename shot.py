import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        # Initialize the shot with position and radius
        super().__init__(x, y, radius)
        self.lifetime = 2000  # Lifetime in milliseconds
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Draw the shot as a small circle
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self, dt):
        # Update position based on velocity and time delta
        self.position += self.velocity * dt
        # Remove the shot if its lifetime has expired
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.kill()
        # Wrap around screen edges
        self.wrap_around_screen()

    def wrap_around_screen(self):
        # Wrap the shot to the opposite side if it moves off-screen
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
