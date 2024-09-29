import pygame
import random
from constants import *
from circleshape import CircleShape
from shot import Shot
from floating_text import FloatingText
from circleshape import Shrapnel
from explosion import Explosion
from text_lists import player_death_screams

class Player(CircleShape):
    def __init__(self, x, y):
        # Initialize the player with position and radius
        super().__init__(x, y, PLAYER_RADIUS)
        self.velocity = pygame.Vector2(0, 0)  # Linear velocity for movement
        self.angular_velocity = 0  # Angular velocity for rotation
        self.rotation = 0  # Initial rotation angle
        self.timer = 0  # Timer for shooting cooldown
        self.score = 0  # Initialize score
        self.time = 0
        self.asteroids_destroyed = 0
        self.health = self.radius * 2
        self.speed = self.velocity.length()
        self.is_player = True
        self.shot_cooldown =    PLAYER_SHOOT_COOLDOWN
        self.shot_damage =      PLAYER_SHOT_DMG
        self.move_speed =       PLAYER_SPEED
        self.turn_speed =       PLAYER_TURN_SPEED
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.right_direction = self.forward_direction.rotate(90)
        # Stabilisers attributes
        self.stabilisers = True  # Set to True to enable stabilisers
        self.stabiliser_str = 0.5  # Strength of stabilisation (tweak this)
        self.forward_velocity = self.velocity.dot(self.forward_direction)
        self.right_velocity = self.velocity.dot(self.right_direction)  # Right velocity relative to facing direction
        self.stabiliser_velocity_threshold = STABILISER_VELOSITY_THRESHOLD
        self.color = PLAYER_COLOR 
    
    def triangle(self):                                               # Calculate the points of the triangle representing the alien ship
        forward = pygame.Vector2(0, 1).rotate(self.rotation)          # Forward direction vector based on the alien's current rotation
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5  # Right direction vector, scaled by the radius
        a = self.position + forward * self.radius                     # Tip of the triangle, positioned forward by the radius
        b = self.position - forward * self.radius - right             # Left corner of the triangle
        c = self.position - forward * self.radius + right             # Right corner of the triangle
        return [a, b, c]                                              # Return the list of triangle points
   
    def draw(self, screen): # Draw the player as a triangle
        points = self.triangle()
        pygame.draw.polygon(screen, (200, 180, 190), points)

    def update(self, dt):
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation) # setting forward direction
        self.right_direction = self.forward_direction.rotate(90)
        self.velocity *= self.friction                                      # Apply linear friction
        self.angular_velocity *= self.angular_friction                      # Apply rotational friction
        self.forward_velocity = self.velocity.dot(self.forward_direction)
        self.right_velocity = self.velocity.dot(self.right_direction)       # Calculate the x-axis velocity (relative to the object's forward direction)
        self.position += self.velocity * dt                                 # Update position based on velocity
        self.rotation += self.angular_velocity * dt                         # Update rotation based on angular velocity
        self.wrap_around_screen()                                           # Wrap around screen edge detection
        self.timer -= dt                                                    # Decrease the shooting timer 
        self.time += dt
                
        keys = pygame.key.get_pressed() # Get the current key states

        # Simplified directional movement and rotation values
        up              = self.move_speed   * dt
        down            = -self.move_speed  * dt
        strafe_left     = -self.move_speed  * dt         # Strafe left
        strafe_right    = self.move_speed   * dt         # Strafe right
        turn_left       = -self.turn_speed  * dt         # Turn left
        turn_right      = self.turn_speed   * dt         # Turn right

        # Key mappings for movement and rotation
        key_up =            keys[pygame.K_w] or keys[pygame.K_UP]       or keys[pygame.K_KP8]
        key_down =          keys[pygame.K_s] or keys[pygame.K_DOWN]     or keys[pygame.K_KP5]
        key_strafe_left =   keys[pygame.K_a]                            or keys[pygame.K_KP4]
        key_strafe_right =  keys[pygame.K_d]                            or keys[pygame.K_KP6]
        key_turn_left =     keys[pygame.K_q] or keys[pygame.K_LEFT]     or keys[pygame.K_KP7]
        key_turn_right =    keys[pygame.K_e] or keys[pygame.K_RIGHT]    or keys[pygame.K_KP9]

        # Handle movement and rotation based on key inputs
        if key_turn_left:       self.apply_torque(turn_left)
        if key_turn_right:      self.apply_torque(turn_right)
        if key_down:            self.move(down)
        if key_up:              self.move(up)
        if key_strafe_left:     self.move_x(strafe_left)            # Move left along the X-axis
        if key_strafe_right:    self.move_x(strafe_right)           # Move right along the X-axis        
        
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()

        if self.stabilisers: 
            self.apply_stabilisers(dt, key_up, key_down, key_strafe_left, key_strafe_right, key_turn_left, key_turn_right)

        if self.health <= 0:
            self.death()
    
    def apply_stabilisers(self, dt, key_up, key_down, key_strafe_left, key_strafe_right, key_turn_left, key_turn_right):
        """
        Applies stabilisation to stop small movements and rotations if no input is provided.

        Args:
            dt (float): The time delta for frame-based updates.
            key_up (bool): Whether the 'move forward' key is pressed.
            key_down (bool): Whether the 'move backward' key is pressed.
            key_strafe_left (bool): Whether the 'strafe left' key is pressed.
            key_strafe_right (bool): Whether the 'strafe right' key is pressed.
            key_turn_left (bool): Whether the 'turn left' key is pressed.
            key_turn_right (bool): Whether the 'turn right' key is pressed.
        """
        # Apply thresholds to stop small movements
        if abs(self.forward_velocity) < self.stabiliser_velocity_threshold:       # Check forward velocity
            self.forward_velocity = 0
        if abs(self.right_velocity) < self.stabiliser_velocity_threshold:         # Check rightward velocity
            self.right_velocity = 0
        if abs(self.angular_velocity) < self.stabiliser_velocity_threshold:       # Check angular velocity
            self.angular_velocity = 0
        # Apply forward/backward stabilisers
        if not key_up and self.forward_velocity > 0:                              # No forward input, moving forward
            self.move(-self.move_speed * dt * self.stabiliser_str)                # Slow down forward movement
        if not key_down and self.forward_velocity < 0:                            # No backward input, moving backward
            self.move(self.move_speed * dt * self.stabiliser_str)                 # Slow down backward movement
        # Apply strafe stabilisers
        if not key_strafe_left and self.right_velocity < 0:                       # No strafe left input, moving left
            self.move_x(self.move_speed * dt * self.stabiliser_str)               # Slow down leftward movement
        if not key_strafe_right and self.right_velocity > 0:                      # No strafe right input, moving right
            self.move_x(-self.move_speed * dt * self.stabiliser_str)              # Slow down rightward movement
        # Apply rotational stabilisers
        if not key_turn_left and self.angular_velocity < 0:                       # No turn left input, rotating left
            self.apply_torque(self.turn_speed * dt * self.stabiliser_str)         # Reduce leftward rotation
        if not key_turn_right and self.angular_velocity > 0:                      # No turn right input, rotating right
            self.apply_torque(-self.turn_speed * dt * self.stabiliser_str)        # Reduce rightward rotation


    def move(self, force_magnitude):
        # Move the player in the direction they are facing
        force = self.forward_direction * force_magnitude
        self.velocity += force  # Apply the force to velocity
        # Create visual effect when moving
        RGB = (255, 0, 0)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        b = self.position - self.forward_direction * self.radius - right
        c = self.position - self.forward_direction * self.radius + right
        FloatingText(b.x, b.y, "^", PLAYER_FIRE_COLOR, 50)
        FloatingText(c.x, c.y, "^", PLAYER_FIRE_COLOR, 50)

    def move_x(self, force_magnitude):
        # Determine the direction relative to player's facing direction
        force = self.right_direction * force_magnitude
        self.velocity += force
        # Check if the force is positive (right) or negative (left)
        self.right_velocity  # Right velocity relative to facing direction
        if force_magnitude > 0:
            force = self.right_direction * force_magnitude  # Move right
            visual_char = ">"  # Right movement, show left-pointing visual effect
        else:
            force = -self.right_direction * abs(force_magnitude)  # Move left
            visual_char = "<"  # Left movement, show right-pointing visual effect
        # Create visual effect when moving horizontally (relative to player's direction)
        right = self.right_direction * self.radius / 1.5
        b = self.position - self.forward_direction * self.radius - right
        c = self.position - self.forward_direction * self.radius + right
        FloatingText(b.x, b.y, visual_char, PLAYER_FIRE_COLOR, 50)
        FloatingText(c.x, c.y, visual_char, PLAYER_FIRE_COLOR, 50)

    def apply_torque(self, torque):
        # Change the angular velocity by applying a torque (for rotation)
        self.angular_velocity += torque

    def apply_force(self, force):
        self.velocity += force

    def wrap_around_screen(self):
        # Wrap the player to the opposite side if they move off-screen
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def shoot(self):
        # Create a new shot in the direction the player is facing
        shot_position = self.position + self.forward_direction * (self.radius + 10) # +10 forward from the ship to avoid collision
        new_shot = Shot((shot_position.x), (shot_position.y), SHOT_RADIUS, self) 
        # Incorporate the player's velocity into the shot's velocity
        new_shot.velocity = PLAYER_SHOT_SPEED * self.forward_direction + self.velocity #add player velocity to shot
        if new_shot.velocity.length() < PLAYER_SHOT_SPEED:
            new_shot.velocity.scale_to_length(PLAYER_SHOT_SPEED) 
        FloatingText(shot_position.x, shot_position.y, "ø", (255, 0, 0), 40)    # Create visual effect when shooting
        self.timer = self.shot_cooldown                                         # Reset the shooting timer

    def death(self):
        scream = random.choice(player_death_screams)
        FloatingText(self.position.x, self.position.y, scream, (250, 200, 100), 2000)
        player_explosion = Explosion(self.position.x, self.position.y, 400)
        self.kill()    

    def bounce(self, other):
        super().bounce(other)

    def destroy_asteroid(self, value):
        self.asteroids_destroyed += value

    def score_points(self, points):
        self.score += points # Points update function

    def get_score(self):
        return self.score # Point getter function

    def get_time(self): 
        return round((self.time), 1) # Get time player has been playing

