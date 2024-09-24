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
        owner = self.owner
        self.is_shot = True

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
        if (self.radius +3) + other.radius > distance:
            self.shot_explode(other, self.owner)
            self.kill()  # Remove the shot after explosion
            
    def shot_explode(self, other, owner):
        """ Method to handle the explosion of the shot, creating shrapnel """
        other.health -= PLAYER_SHOT_DMG
        print(f"shot exploded on {other} with damage {PLAYER_SHOT_DMG}")
        self.shrapnel_obj(self.radius, (150, 10, 15))  # Create shrapnel pieces when the shot explodes
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

        