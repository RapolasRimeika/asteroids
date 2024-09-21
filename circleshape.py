import pygame

# Base class for circular game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # Initialize sprite and add to groups if containers are set
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # Subclasses should override this method to draw themselves
        pass

    def update(self, dt):
        # Subclasses should override this method to update themselves
        pass

    def collision(self, other):
        # Check for collision with another CircleShape
        distance = self.position.distance_to(other.position)
        return self.radius + other.radius > distance
