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
        bounce = False
        distance = self.position.distance_to(other.position)
        if (self.radius + 3) + other.radius > distance:
            self.shot_score(other, self.owner)
            self.shot_explode()    

    def shot_explode(self):
        explosion = Explosion(self.position.x, self.position.y, 200)  # Create the explosion object
        self.shrapnel_obj(self.radius, (150, 10, 15))
        self.kill()

    def apply_torque(self, torque):
        pass

    def draw(self, screen):
        # Draw the shot as a small circle
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)
        back_pos = self.position + self.forward_direction.rotate(180) * self.radius
        RGB = (255, 0, 0)
        FloatingText(self.back_pos.x, self.back_pos.y, "*", RGB, 40)

    def shot_score(self, other, owner):
        other.health -= owner.shot_damage
        print(f"shot exploded on {other} with damage {PLAYER_SHOT_DMG}")
        if hasattr(other, "isalien") and other.isalien == True and other.health <= 0:
            print(f"KILL ALIEN CONFIRMED by OWNER{owner} {round(other.health)}")
            owner.score += 5
            print(f"Player's new score: {owner.score}")
            return True
        elif other.health <= 0:
            print(f"KILL CONFIRMED OWNER{owner} {round(other.health)}")
            owner.score += 1
            print(f"Player's new score: {owner.score}")
            return True
        self.shrapnel_obj(self.radius)  # Create shrapnel pieces when the shot explodes

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

