import pygame
from circleshape import CircleShape
from constants import *
from floating_text import FloatingText
from explosion import Explosion

class Shot(CircleShape):
    """
    The Shot class represents a projectile fired in the game, inheriting from CircleShape. 
    It manages the shot's position, lifetime, and interactions with other game objects 
    through collisions and explosions.     
    Methods:
        update(dt): Updates the shot's position, checks lifetime expiration.
        collision(other, bounce=True): Handles collisions with other objects.
        shot_explode(other): Explodes the shot on collision.
        shot_score(other, owner): Updates the score when a shot kills an object.
        apply_torque(torque): Disables angular velocity for the shot.
        draw(screen): Draws the shot on the screen.
        get_backward_pos(): Gets the position behind the shot for visual effects.
    """
    def __init__(self, x, y, radius, owner):
        super().__init__(x, y, radius)                                      # Initialize the shot with position and radius
        self.lifetime = SHOT_LIFETIME                                       # Set the lifetime of the shot
        self.spawn_time = pygame.time.get_ticks()                           # Record the spawn time for shot expiration
        self.owner = owner                                                  # Set the owner of the shot
        owner = self.owner                                                  # Assign owner to local variable
        self.is_shot = True                                                 # Mark this object as a shot
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation) # Set the forward direction based on rotation
        self.forward_velocity = self.velocity.dot(self.forward_direction)   # Calculate forward velocity along direction
        self.back_pos = self.get_backward_pos()                             # Get position at the backward-facing point
        self.color = (250, 0, 0)                                            # Set the shot's color to red

    def update(self, dt):
        self.angular_velocity = 0                                           # Disable angular velocity (no rotation for the shot)
        super().update(dt)                                                  # Call the parent class update for position and velocity
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation) # Update the forward direction based on current rotation
        self.forward_velocity = self.velocity.dot(self.forward_direction)   # Calculate forward velocity along the direction
        self.back_pos = self.get_backward_pos()                             # Get the position at the backward-facing point      
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:                  # Check if the shot's lifetime has expired
            self.kill()                                                     # Remove the shot if its lifetime has expired
        
    def collision(self, other, bounce=True):
        if hasattr(other, "is_explosion") and other.is_explosion == True:   # Ignore collisions with explosion objects
            return
        bounce = False                                                      # Disable bounce for the shot
        distance = self.position.distance_to(other.position)                # Calculate the distance between the shot and the other object
        if self.radius + other.radius > distance - SHOT_EXPLOSION_BUFFER:   # Check for collision, buffer allows explosion before impact
            self.shot_explode(other)                                        # Trigger shot explosion on collision

    def shot_explode(self, other):
        if self.owner != other:                                             # Prevent the shot from hitting its owner
            print(f"other health before shot: {other.health}")              # Log the target's health before applying damage
            other.health -= self.owner.shot_damage                          # Apply the shot's damage to the other object
            self.shot_score(other, self.owner)                              # Update the score based on the outcome
            print(f"other health after shot: {other.health}")               # Log the target's health after damage
            explosion = Explosion(self.position.x, self.position.y)         # Create an explosion at the shot's position
            self.shrapnel_obj(self.radius)                                  # Generate shrapnel after the explosion

    def shot_score(self, other, owner):
        print(f"shot exploded on {other} with damage {PLAYER_SHOT_DMG}")                # Log explosion event with damage details
        if hasattr(other, "isalien") and other.isalien == True and other.health <= 0:   # Check if target is an alien and is dead
            owner.score += 5                                                            # Award 5 points for killing an alien
            other.shrapnel_obj(other.radius)                                            # Trigger shrapnel generation on alien's death
            print(f"KILL ALIEN CONFIRMED by OWNER {owner} {round(other.health)}")       # Log alien kill confirmation
            print(f"Player's new score: {owner.score}")                                 # Log the updated player score
        elif other.health <= 0:                                                         # Check if a non-alien object is dead
            owner.score += 1                                                            # Award 1 point for killing a non-alien object
            other.shrapnel_obj(other.radius)                                            # Trigger shrapnel generation on non-alien death
            print(f"KILL CONFIRMED OWNER {owner} {round(other.health)}")                # Log kill confirmation
            print(f"Player's new score: {owner.score}")                                 # Log the updated player score

    def apply_torque(self, torque):
        pass

    def draw(self, screen):
        # Draw the shot as a small circle
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, 2)
        back_pos = self.position + self.forward_direction.rotate(180) * self.radius
        RGB = (255, 0, 0)
        FloatingText(self.back_pos.x, self.back_pos.y, "*", RGB, 40)

    def get_backward_pos(self):
        if self.velocity.length() > 0:                                          # Normalize forward velocity to get the direction
            forward_direction = self.velocity.normalize()                       # (avoid division by zero)
        else:
            forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)      # Use rotation for forward direction if stationary
        backward_direction = -forward_direction                                 # Reverse the direction to get the backward direction
        backward_position = self.position + backward_direction * self.radius    # Calculate position at the backward-facing point
        return backward_position                                                # Return the calculated backward position


