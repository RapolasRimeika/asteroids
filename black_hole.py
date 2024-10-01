import pygame
from circle_shape import CircleShape
from constants import *

class BlackHole(CircleShape):
    """ 
    The BLK class represents a black hole object that pulls other objects 
    within its radius and can destroy them if they get too close. Inherits 
    from CircleShape for physical properties and movement.
    """
    def __init__(self):
        super().__init__(BLACK_HOLE_X, BLACK_HOLE_Y, BLACK_HOLE_RADIUS, BLACK_HOLE_FRICTION, BLACK_HOLE_ANGULAR_FRICTION)
        self.is_explosion = True                                           # Mark the black hole as an explosion type object
        self.color =        BLACK_HOLE_COLOR                               # Set the color of the black hole
        self.health =       BLACK_HOLE_HEALTH                              # Set the initial health for the black hole
        self.radius =       BLACK_HOLE_RADIUS                              # Set the radius for the black hole
        self.near =         BLACK_HOLE_NEAR                                # Near range where the pull force is strongest
        self.mid_radius =   BLACK_HOLE_MID_RADIUS                          # Mid-range radius for medium pull force
        self.far_radius =   BLACK_HOLE_FAR_RADIUS                          # Far range where the pull force is weakest
        self.colli_buffer = BLACK_HOLE_COLLI_BUFFER                        # Collision buffer for absorbing objects at close range
        self.near_pull =    BLACK_HOLE_NEAR_PULL                           # Pull strength for near range
        self.mid_pull =     BLACK_HOLE_MID_PULL                            # Pull strength for mid-range
        self.far_pull =     BLACK_HOLE_FAR_PULL                            # Pull strength for far range

    def update(self, dt):
        super().update(dt)                                                 # Update the black hole's position and velocity
        if self.health < 5000:                                             # Regenerate black hole health if below a threshold
            self.health += 1000

    def collision(self, other):
        print(f"Black hole swallowed {other}")                             # Log object being pulled by the black hole
        distance = self.position.distance_to(other.position)               # Calculate the distance between the black hole and another object
        if distance <= self.far_radius + other.radius:                     # If within the influence range
            if distance <= self.radius + self.colli_buffer:                # If within the death radius of the black hole
                other.kill()                                               # Destroy the object
            if distance <= self.near:                                      # Apply the strongest pull force for near range
                strength = self.near_pull
                self.calculate_force(other, strength)
            elif distance <= self.mid_radius:                              # Apply medium pull force for mid-range
                strength = self.mid_pull
                self.calculate_force(other, strength)
            else:                                                          # Apply the weakest pull force for far range
                strength = self.far_pull
                self.calculate_force(other, strength)

        bounce = False                                                     # Disable bounce when colliding with the black hole

    def calculate_force(self, other, strength):
        explosion_vector = other.position - self.position                  # Calculate vector direction of the pull
        if explosion_vector.length() > 0:
            explosion_vector.normalize_ip()                                # Normalize vector to get the direction
        force = explosion_vector * strength                                # Multiply by strength to get the pull force
        other.apply_force(force)                                           # Apply the calculated force to the object

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (int(self.position.x + 1), int(self.position.y + 1)), self.radius)
        """FOR debugging only 
        # Draw the influence radius lines (near, mid, and far radii)
        for radius in [self.near, self.mid_radius, self.far_radius]:
            pygame.draw.circle(screen, self.color,  # Use the color for the lines
                (int(self.position.x + 1), int(self.position.y + 1)),  # Position
                int(radius), 2  # Radius and thickness of the line
            )"""

    def apply_force(self, force):
        pass                                                               # No additional forces applied by the black hole directly
