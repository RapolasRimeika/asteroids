import pygame
import random

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

    def collision(self, other, bounce=True):
        # Check for collision with another CircleShape
        distance = self.position.distance_to(other.position)
        if self.radius + other.radius > distance:
            if bounce == True:
                self.bounce(other)
            return True

    def bounce(self, other):       
        # Calculate the normal vector (line of impact)
        normal = self.position - other.position
        # Normalize the normal vector
        normal_distance = normal.length()
        if normal_distance == 0:
            # Avoid division by zero; choose an arbitrary normal vector
            normal = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            normal.normalize_ip()
        else:
            normal /= normal_distance  # Normalize

        # Calculate relative velocity
        relative_velocity = self.velocity - other.velocity

        # Calculate velocity along the normal
        velocity_along_normal = relative_velocity.dot(normal)

        # Do not resolve if velocities are separating
        if velocity_along_normal > 0:
            return

        # Calculate restitution (elasticity of the collision)
        restitution = 1  # 1 for perfectly elastic collision, 0 for perfectly inelastic

        # Calculate masses (using radius as mass or radius squared)
        mass_self = self.radius  # Or self.radius ** 2
        mass_other = other.radius  # Or other.radius ** 2

        # Calculate impulse scalar
        impulse_scalar = -(1 + restitution) * velocity_along_normal
        impulse_scalar /= (1 / mass_self + 1 / mass_other)

        # Calculate impulse vector
        impulse = impulse_scalar * normal

        # Update velocities
        self.velocity += (impulse / mass_self)
        other.velocity -= (impulse / mass_other)
    