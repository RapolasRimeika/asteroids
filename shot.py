import pygame
from circleshape import CircleShape
from constants import *
from floating_text import FloatingText
from explosion import Explosion

class Shot(CircleShape):
    def __init__(self, x, y, radius, owner):
        # Initialize the shot with position and radius
        super().__init__(x, y, radius)
        self.lifetime = SHOT_LIFETIME
        self.spawn_time = pygame.time.get_ticks()
        self.owner = owner
        owner = self.owner
        self.is_shot = True
        self.angular_velocity = 0  # Disable angular velocity
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.forward_velocity = self.velocity.dot(self.forward_direction)
        self.back_pos = self.get_backward_pos()
        self.color = (250, 0, 0)

    def update(self, dt):
        self.position += self.velocity * dt # Update position based on velocity and time delta
        self.velocity *= self.friction # Apply linear friction to slow down movement over time
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.forward_velocity = self.velocity.dot(self.forward_direction)
        self.back_pos = self.get_backward_pos()
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime: # Remove the shot if its lifetime has expired
            self.kill()
        
    def collision(self, other, bounce=True):
        if hasattr(other, "is_explosion") and other.is_explosion == True:
            return
        bounce = False
        distance = self.position.distance_to(other.position)
        if self.radius + other.radius > distance -5:                # Check collision, -5 explode before colision
            self.shot_explode(other)                                # Trigger explosion on collision

    def shot_explode(self, other):
        if self.owner != other:                                     # Prevent self-hit
            print(f"other health before shot: {other.health}")
            other.health -= self.owner.shot_damage                  # Apply shot damage to the other object
            self.shot_score(other, self.owner)                      # Update score
            print(f"other health after shot: {other.health}")
            explosion = Explosion(self.position.x, self.position.y) # Create explosion force
            self.shrapnel_obj(10)                                   # Create Shrapnel

    def shot_score(self, other, owner):
        print(f"shot exploded on {other} with damage {PLAYER_SHOT_DMG}")
        if hasattr(other, "isalien") and other.isalien == True and other.health <= 0:  # Check if target is alien and dead
            owner.score += 5                                        # Alien kill gives 5 points
            other.shrapnel_obj(other.radius)
            print(f"KILL ALIEN CONFIRMED by OWNER {owner} {round(other.health)}")
            print(f"Player's new score: {owner.score}")
        elif other.health <= 0:                                     # Check if non-alien object is dead
            owner.score += 1                                        # Non-alien kill gives 1 point
            other.shrapnel_obj(other.radius)
            print(f"KILL CONFIRMED OWNER {owner} {round(other.health)}")
            print(f"Player's new score: {owner.score}")


    def apply_torque(self, torque):
        pass

    def draw(self, screen):
        # Draw the shot as a small circle
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)
        back_pos = self.position + self.forward_direction.rotate(180) * self.radius
        RGB = (255, 0, 0)
        FloatingText(self.back_pos.x, self.back_pos.y, "*", RGB, 40)

    def get_backward_pos(self):
        # Normalize the forward velocity to get the direction (avoid division by zero)
        if self.velocity.length() > 0:
            forward_direction = self.velocity.normalize()
        else:
            forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        # Reverse the direction to get the backward direction
        backward_direction = -forward_direction

        # Calculate the position at the backward-facing point on the circle's radius
        backward_position = self.position + backward_direction * self.radius

        return backward_position

