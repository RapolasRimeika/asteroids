import pygame
from circleshape import CircleShape
from constants import *
from floating_text import FloatingText

class Shot(CircleShape):
    def __init__(self, x, y, radius, owner):
        # Initialize the shot with position and radius
        super().__init__(x, y, radius)
        self.lifetime = 2000  # Lifetime in milliseconds
        self.spawn_time = pygame.time.get_ticks()
        self.owner = owner

        # Disable angular velocity
        self.angular_velocity = 0

    def update(self, dt):
        # Update position based on velocity and time delta
        self.position += self.velocity * dt
        
        # Apply linear friction to slow down movement over time
        self.velocity *= self.friction

        # Remove the shot if its lifetime has expired
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.kill()

    def apply_torque(self, torque):
        # Override to do nothing, so no angular momentum is applied
        pass

    def draw(self, screen):
        # Draw the shot as a small circle
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)
        RGB = (255, 0, 0)
        FloatingText(self.position.x, self.position.y, ".", RGB, 40)

    def collision(self, other, bounce=True):
        # Check for collision with another CircleShape
        bounce = False
        distance = self.position.distance_to(other.position)
        if self.radius + other.radius > distance:
            self.shot_explode(other)
            self.kill()  # Remove the shot after explosion

    def shot_explode(self, other):
        """ Method to handle the explosion of the shot, creating shrapnel """
        self.shrapnel_obj(self.radius)  # Create shrapnel pieces when the shot explodes
        other.health -= PLAYER_SHOT_DMG
        print(f"shot exploded on {other} with damage {PLAYER_SHOT_DMG}")
        if other.health <= 0:
            print(f"Other health now {round(other.health)}")
            return True
