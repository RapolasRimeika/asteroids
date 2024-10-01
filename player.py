import pygame
import random
from constants import *
from circle_shape import CircleShape
from shot import Shot
from floating_text import FloatingText
from explosion import Explosion
from text_lists import player_death_screams

class Player(CircleShape):
    """
    The Player class represents the player's spaceship in the game, inheriting from CircleShape.
    It handles movement, shooting, scoring, and interaction with game elements such as asteroids.
    The player can move, rotate, shoot projectiles, and is affected by friction and stabilisers.
    """
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)                                   # Initialize the player with position and radius
        self.velocity = pygame.Vector2(0, 0)                                    # Linear velocity for movement
        self.angular_velocity = 0                                               # Angular velocity for rotation
        self.rotation = 0                                                       # Initial rotation angle
        self.timer = 0                                                          # Timer for shooting cooldown
        self.score = 0                                                          # Initialize player's score
        self.time = 0                                                           # Track the player's time in the game
        self.asteroids_destroyed = 0                                            # Track the number of asteroids destroyed
        self.health = self.radius * 2                                           # Set health based on player radius
        self.speed = self.velocity.length()                                     # Speed is the magnitude of the velocity
        self.is_player = True                                                   # Flag to identify the object as a player
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN                              # Set the cooldown time between shots
        self.shot_damage = PLAYER_SHOT_DMG                                      # Set the damage caused by player's shot
        self.move_speed = PLAYER_SPEED                                          # Set the player's movement speed
        self.turn_speed = PLAYER_TURN_SPEED                                     # Set the player's turning speed
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)     # Forward direction vector based on current rotation
        self.right_direction = self.forward_direction.rotate(90)                # Right direction vector (perpendicular to forward)       
        self.stabiliser_str = STABILISER_STR                                    # Set the strength of the stabilisers
        self.forward_velocity = self.velocity.dot(self.forward_direction)       # Calculate forward velocity relative to direction
        self.right_velocity = self.velocity.dot(self.right_direction)           # Calculate right velocity relative to direction
        self.stabiliser_velocity_threshold = STABILISER_VELOSITY_THRESHOLD      # Threshold for stabilising velocity
        self.color = PLAYER_COLOR                                               # Set the player's color

    def triangle(self):                                                         # Calculate the points of the triangle representing the alien ship
        forward = pygame.Vector2(0, 1).rotate(self.rotation)                    # Forward direction vector based on the alien's current rotation
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5  # Right direction vector, scaled by the radius
        a = self.position + forward * self.radius                               # Tip of the triangle, positioned forward by the radius
        b = self.position - forward * self.radius - right                       # Left corner of the triangle
        c = self.position - forward * self.radius + right                       # Right corner of the triangle
        return [a, b, c]                                                        # Return the list of triangle points
   
    def draw(self, screen):                                                     # Draw the player as a triangle
        points = self.triangle()
        pygame.draw.polygon(screen, (200, 180, 190), points)

    def update(self, dt):
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)     # Set the forward direction based on rotation
        self.right_direction = self.forward_direction.rotate(90)                # Set the right direction (perpendicular to forward)
        self.velocity *= self.friction                                          # Apply linear friction to reduce movement over time
        self.angular_velocity *= self.angular_friction                          # Apply rotational friction to slow down turning
        self.forward_velocity = self.velocity.dot(self.forward_direction)       # Calculate forward velocity relative to facing direction
        self.right_velocity = self.velocity.dot(self.right_direction)           # Calculate rightward velocity relative to facing direction
        self.position += self.velocity * dt                                     # Update position based on velocity and time delta
        self.rotation += self.angular_velocity * dt                             # Update rotation based on angular velocity
        self.wrap_around_screen()                                               # Ensure player wraps around screen edges
        self.timer -= dt                                                        # Decrease the shooting cooldown timer
        self.time += dt                                                         # Track the total time the player has been in the game
        self.handle_input(dt)                                                   # Handle key inputs and movement
    
    def handle_input(self, dt):
        # This method handles key inputs and movement
        keys = pygame.key.get_pressed()                                       # Get the current key states
        up              = self.move_speed   * dt
        down            = -self.move_speed  * dt
        strafe_left     = -self.move_speed  * dt
        strafe_right    = self.move_speed   * dt
        turn_left       = -self.turn_speed  * dt
        turn_right      = self.turn_speed   * dt

        key_up = any(keys[key] for key in KEY_UP)
        key_down = any(keys[key] for key in KEY_DOWN)
        key_strafe_left = any(keys[key] for key in KEY_STRAFE_LEFT)
        key_strafe_right = any(keys[key] for key in KEY_STRAFE_RIGHT)
        key_turn_left = any(keys[key] for key in KEY_TURN_LEFT)
        key_turn_right = any(keys[key] for key in KEY_TURN_RIGHT)

        # Apply movements based on key input
        if key_turn_left:       self.apply_torque(turn_left)
        if key_turn_right:      self.apply_torque(turn_right)
        if key_down:            self.move(down)
        if key_up:              self.move(up)
        if key_strafe_left:     self.move_x(strafe_left)
        if key_strafe_right:    self.move_x(strafe_right)

        if keys[KEY_SHOOT] and self.timer <= 0:
            self.shoot()
        self.apply_stabilisers(dt, key_up, key_down, key_strafe_left, key_strafe_right, key_turn_left, key_turn_right)

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
        force = self.forward_direction * force_magnitude                          # Calculate force in forward direction
        self.velocity += force                                                    # Apply the force to the player's velocity
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5  # Right offset for visual effect
        b = self.position - self.forward_direction * self.radius - right          # Left-side effect position
        c = self.position - self.forward_direction * self.radius + right          # Right-side effect position
        FloatingText(b.x, b.y, "^", PLAYER_FIRE_COLOR, 50)                        # Show left-side visual effect
        FloatingText(c.x, c.y, "^", PLAYER_FIRE_COLOR, 50)                        # Show right-side visual effect

    def move_x(self, force_magnitude):
        force = self.right_direction * force_magnitude                            # Calculate force in right direction
        self.velocity += force                                                    # Apply force to player's velocity
        self.right_velocity                                                       # Right velocity relative to facing direction
        if force_magnitude > 0:                                                   # Moving right
            force = self.right_direction * force_magnitude                        # Adjust movement to the right
            visual_char = ">"                                                     # Show right movement effect
        else:                                                                     # Moving left
            force = -self.right_direction * abs(force_magnitude)                  # Adjust movement to the left
            visual_char = "<"                                                     # Show left movement effect
        right = self.right_direction * self.radius / 1.5                          # Right offset for visual effect
        b = self.position - self.forward_direction * self.radius - right          # Left-side effect position
        c = self.position - self.forward_direction * self.radius + right          # Right-side effect position
        FloatingText(b.x, b.y, visual_char, PLAYER_FIRE_COLOR, 50)                # Show left-side visual effect
        FloatingText(c.x, c.y, visual_char, PLAYER_FIRE_COLOR, 50)                # Show right-side visual effect


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
        scream = random.choice(player_death_screams)                               # Choose a random death scream
        FloatingText(self.position.x, self.position.y, scream, (250, 200, 100), 2000) # Display floating text at player's position
        player_explosion = Explosion(self.position.x, self.position.y, 400)       # Create an explosion at player's position
        self.kill()                                                               # Remove the player object from the game

    def shrapnel_obj(self, mass):
        """
        Player's custom shrapnel generation, including death logic.
        """
        if self.destroyed:                                                        # Check if the player is already destroyed
            return                                                                # Exit if destroyed to avoid multiple calls
        self.kill()                                                               # Remove the player object
        self.destroyed = True                                                     # Mark the player as destroyed
        self.death()                                                              # Call the player's death method
        self.create_shrapnel(mass)                                                # Generate shrapnel using the provided mass

    def destroy_asteroid(self, value):
        self.asteroids_destroyed += value                                         # Increment the number of asteroids destroyed by the given value
    def score_points(self, points):
        self.score += points                                                      # Increment the player's score by the given points
    def get_score(self):
        return self.score                                                         # Return the player's current score
    def get_time(self): 
        return round((self.time), 1)                                              # Return the player's playtime, rounded to one decimal place
