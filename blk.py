import pygame
from circleshape import CircleShape
from constants import *

class BLK(CircleShape):
    def __init__(self):
        super().__init__(BLACK_HOLE_X, BLACK_HOLE_Y, BLACK_HOLE_RADIUS, BLACK_HOLE_FRICTION, BLACK_HOLE_ANGULAR_FRICTION)
        self.is_explosion = True
        self.color =        BLACK_HOLE_COLOR
        self.health =       BLACK_HOLE_HEALTH
        self.radius =       BLACK_HOLE_RADIUS
        self.near =         BLACK_HOLE_NEAR
        self.mid_radius =   BLACK_HOLE_MID_RADIUS
        self.far_radius =   BLACK_HOLE_FAR_RADIUS
        self.colli_buffer = BLACK_HOLE_COLLI_BUFFER
        self.near_pull =    BLACK_HOLE_NEAR_PULL
        self.mid_pull =     BLACK_HOLE_MID_PULL
        self.far_pull =     BLACK_HOLE_FAR_PULL

    def update(self, dt):
        super().update(dt)
        if self.health < 5000:                              # Keep the black hole
            self.health += 1000

    def collision(self, other):
        print(f"Black hole swallowed {other}")
        distance = self.position.distance_to(other.position)
        if distance <= self.far_radius + other.radius:      # Within range
            if distance <= self.radius + self.colli_buffer: # Black hole death radius
                other.kill()
            if distance <= self.near:                         # Close range
                strength = self.near_pull
                self.calculate_force(other, strength)
            elif distance <= self.mid_radius:               # Mid range
                strength = self.mid_pull
                self.calculate_force(other, strength)
            else:                                           # Far range
                strength = self.far_pull
                self.calculate_force(other, strength)

        bounce = False

    def calculate_force(self, other, strength):             # Apply force based on distance
        explosion_vector = other.position - self.position
        if explosion_vector.length() > 0:
            explosion_vector.normalize_ip()
        force = explosion_vector * strength
        other.apply_force(force)

    def draw(self, screen):
        # Draw the black filled circle at the center of the black hole
        pygame.draw.circle(screen, (0, 0, 0), (int(self.position.x + 1), int(self.position.y + 1)), self.radius)
        
        """FOR debugging only # Draw the influence radius lines (near, mid, and far radii)
        for radius in [self.near, self.mid_radius, self.far_radius]:
            pygame.draw.circle(
                screen, self.color,  # Use the color for the lines
                (int(self.position.x + 1), int(self.position.y + 1)),  # Position
                int(radius), 2  # Radius and thickness of the line
            )"""
    def apply_force(self, force):
        pass  #here it's inherited from CircleShape
