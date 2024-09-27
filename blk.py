import pygame
from circleshape import CircleShape

class BLK(CircleShape):
    def __init__(self):
        x = 100
        y = 100
        radius = 75
        friction = 1
        angular_friction = 1
        super().__init__(x, y, radius, friction, angular_friction)
        
        self.is_explosion = True
        self.far_radius = 700
        self.near = self.far_radius / 4
        self.mid_radius = self.far_radius / 2
        self.color = (150, 120, 160)
        self.health = 1_000_000_000_000_000  

    def update(self, dt):
        super().update(dt)
        if self.health < 5000:
            self.health += 1000

    def collision(self, other):
        print(f"Explosion colliding with {other}")
        distance = self.position.distance_to(other.position)
        self.radius = 100  # Ensure radius is consistent

        if distance <= self.far_radius + other.radius:  # Within range
            if distance <= self.radius:
                other.kill()
            if distance <= self.near:  # Close range
                strength = -1
                self.calculate_force(other, strength)
            elif distance <= self.mid_radius:  # Mid range
                strength = -0.1
                self.calculate_force(other, strength)
            else:  # Far range
                strength = -0.03
                self.calculate_force(other, strength)

        bounce = False

    def calculate_force(self, other, strength):
        """Apply force to the object based on proximity."""
        explosion_vector = other.position - self.position
        if explosion_vector.length() > 0:
            explosion_vector.normalize_ip()
        force = explosion_vector * strength * 100  # Scale force
        other.apply_force(force)

    def draw(self, screen):
        """Visualize the black hole and its influence radius on the screen."""
        # Draw the black filled circle at the center of the black hole
        pygame.draw.circle(
            screen, (0, 0, 0),  # Black color for the filled circle
            (int(self.position.x + 1), int(self.position.y + 1)),  # Position
            self.radius  # Radius of the black hole (filled circle)
        )
        
        """# Draw the influence radius lines (near, mid, and far radii)
        for radius in [self.near, self.mid_radius, self.far_radius]:
            pygame.draw.circle(
                screen, self.color,  # Use the color for the lines
                (int(self.position.x + 1), int(self.position.y + 1)),  # Position
                int(radius), 2  # Radius and thickness of the line
            )
"""
    def apply_force(self, force):
        pass  # Override if necessary; here it's inherited from CircleShape
