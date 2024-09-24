import pygame
from floating_text import FloatingText

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, far_radius):
        # Automatically add the Explosion to the appropriate groups
        super().__init__(self.containers if hasattr(self, "containers") else None)
        self.is_explosion = True
        # Set position and explosion properties
        self.position = pygame.Vector2(x, y)
        self.near = far_radius / 4
        self.mid_radius = far_radius / 2
        self.far_radius = far_radius

        # Create groups for different ranges
        self.near_group = pygame.sprite.Group()
        self.mid_group = pygame.sprite.Group()
        self.far_group = pygame.sprite.Group()
        self.color = (189, 12, 16)
        self.radius = 1  # Explosion's own radius for collision detection

    def update(self, dt):
        """ Placeholder for updates if needed later """
        pass

    def collision(self, other, bounce=True):
        """ Check collision, categorize objects, and apply force """
        distance = self.position.distance_to(other.position)

        if distance <= self.far_radius + other.radius:
            if distance <= self.near:
                self.near_group.add(other)
                strength = 1.0  # Full force
            elif distance <= self.mid_radius:
                self.mid_group.add(other)
                strength = 0.5  # Medium force
            else:
                self.far_group.add(other)
                strength = 0.2  # Weak force
            self.calculate_force(other, strength)
        self.kill()  # Remove the explosion after applying force

    def calculate_force(self, other, strength):
        """ Apply force to the object based on proximity """
        explosion_vector = other.position - self.position
        if explosion_vector.length() > 0:
            explosion_vector.normalize_ip()
        force = explosion_vector * strength * 100  # Scale force
        other.apply_force(force)

    def draw(self, screen):
        """ Visualize the explosion radius on the screen """
        for radius in [self.near, self.mid_radius, self.far_radius]:
            pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), int(radius), 1)

    def apply_force(self, other):
        pass