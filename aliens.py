import pygame
import random
from constants import *
from circleshape import CircleShape
from shot import Shot
from floating_text import FloatingText
from circleshape import Shrapnel
from text_lists import alien_screams
from loot import LootSpawner
from explosion import Explosion

class AlienShip(CircleShape):
    class AlienShip(CircleShape):
        """
        Represents an AI-controlled alien ship that targets the player and avoids asteroids.

        The `AlienShip` class extends the `CircleShape` class and manages all the behaviors related to
        an alien ship, including movement, shooting, avoiding obstacles, and handling death. The alien ship
        moves towards the player, adjusts its path to avoid asteroids, and shoots at the player and nearby
        asteroids within range. It also uses stabilizers to maintain control over small movements and rotation.

        Methods:
            triangle(): Calculates the points of the triangle used to represent the alien ship on screen.
            draw(screen): Renders the alien ship as a triangle on the screen.
            update(dt): Updates the alien ship's position, rotation, and behavior each frame.
            avoid_asteroids(dt): Adjusts the alien's movement to avoid nearby asteroids.
            move_towards_player(dt): Moves the alien towards the player's position.
            move(force_magnitude): Moves the alien in the direction it is facing by applying a force.
            apply_torque(torque): Changes the alien's angular velocity by applying a rotational force.
            shoot_if_in_range(): Shoots at the player or nearby asteroids if within range and facing them.
            shoot_at(target): Fires a shot at the specified target if the alien is facing it.
            death(): Handles the alien's death, including visual effects, spawning shrapnel, and dropping loot.
        """


    def __init__(self, x, y, ALIEN_RADIUS, player_target, asteroids):
        super().__init__(x, y, ALIEN_RADIUS)
        self.isalien =          True                            # Flag to mark this object as an alien ship
        self.color =            ALIEN_COLOR                     # The color of the alien ship for rendering
        self.move_speed =       ALIEN_MOVE_SPEED                # Speed at which the alien ship moves
        self.turn_speed =       ALIEN_TURN_SPEED                # Speed at which the alien ship turns/rotates
        self.shooting_range =   ALIEN_SHOOTING_RANGE            # Max range to shoot at player or asteroids
        self.shot_damage =      PLAYER_SHOT_DMG                 # Damage dealt by each shot fired by the alien
        self.health =           ALIEN_HEALTH                    # Health of the alien ship
        self.max_speed =        ALIEN_MAX_SPEED                 # Maximum speed the alien ship can reach
        self.max_ang_velocity = ALIEN_MAX_ANGULAR_VELOCITY      # Maximum rotational speed for the alien
        self.target = player_target                             # Reference to the player object
        self.asteroids = asteroids                              # List of asteroid objects in the game
        self.timer = 0                                          # Shooting cooldown timer
        self.angular_velocity = 0                               # Initial angular velocity (rotation speed)
        self.forward_velocity = 0                               # Initial forward velocity of the alien ship
        self.right_velocity = 0                                 # Initial rightward velocity of the alien ship
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.right_direction = self.forward_direction.rotate(90)
        self.stabiliser_str = ALIEN_STABILISER_STRENGTH         # Strength of stabilisation
        self.score =0
        self.velocity_threshold = STABILISER_VELOSITY_THRESHOLD

    def triangle(self):                                               # Calculate the points of the triangle representing the alien ship
        forward = pygame.Vector2(0, 1).rotate(self.rotation)          # Forward direction vector based on the alien's current rotation
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5  # Right direction vector, scaled by the radius
        a = self.position + forward * self.radius                     # Tip of the triangle, positioned forward by the radius
        b = self.position - forward * self.radius - right             # Left corner of the triangle
        c = self.position - forward * self.radius + right             # Right corner of the triangle
        return [a, b, c]                                              # Return the list of triangle points

    def draw(self, screen):
        points = self.triangle()                                      # Draw the alien ship as a triangle
        pygame.draw.polygon(screen, self.color, points)

    def update(self, dt):
        # Update the forward and right directions based on current rotation
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)   # Update forward direction based on rotation
        self.right_direction = self.forward_direction.rotate(90)              # Right direction is perpendicular to forward
        # Apply friction to linear and angular velocities
        self.velocity *= self.friction                                      # Apply friction to the linear velocity
        self.angular_velocity *= self.angular_friction                      # Apply friction to the angular velocity
        # Calculate velocities relative to the ship's facing direction
        self.forward_velocity = self.velocity.dot(self.forward_direction)   # Calculate forward velocity component
        self.right_velocity = self.velocity.dot(self.right_direction)       # Calculate rightward velocity component
        # Clamp velocities to maximum values
        if self.velocity.length() > self.max_speed:                         # Ensure velocity doesn't exceed max speed
            self.velocity.scale_to_length(self.max_speed)                   # Scale velocity to max speed if necessary
        self.angular_velocity = max(-self.max_ang_velocity, min(self.angular_velocity, self.max_ang_velocity))  # Clamp angular velocity
        # Update position and rotation based on velocities
        self.position += self.velocity * dt                                 # Update position based on velocity and time delta
        self.rotation += self.angular_velocity * dt                         # Update rotation based on angular velocity
        self.rotation %= 360                                                # Keep rotation within 0 to 360 degrees
        self.timer -= dt                                                    # Decrease shooting cooldown timer
        # Flags to determine if the alien is actively moving or rotating
        self.is_moving_forward = False                                      # Reset forward movement flag
        self.is_rotating = False                                            # Reset rotation flag
        # Move the alien ship based on its behavior
        self.avoid_asteroids(dt)                                            # Call method to avoid asteroids
        self.move_towards_player(dt)                                        # Call method to move towards the player
        self.shoot_if_in_range()                                            # Shoot if within range, or shoot nearby asteroids
        self.stabilise(dt)                                                  # Apply stabilisation logic to smooth movements

    def stabilise(self, dt):
        """ Applies stabilisers to reduce small movements and rotational drifts if enabled.
        Args: dt (float): The time delta for frame-based updates."""
        if abs(self.forward_velocity) < self.velocity_threshold:                    # Stop forward movement if below threshold
            self.forward_velocity = 0
        if abs(self.right_velocity) < self.velocity_threshold:                      # Stop rightward movement if below threshold
            self.right_velocity = 0
        if abs(self.angular_velocity) < self.velocity_threshold:                    # Stop angular movement if below threshold
            self.angular_velocity = 0
        if not self.is_moving_forward:                                              # If not actively moving forward
            if self.forward_velocity > 0:
                self.move(-self.move_speed * dt * self.stabiliser_str)              # Stabilise forward movement
            elif self.forward_velocity < 0:
                self.move(self.move_speed * dt * self.stabiliser_str)               # Stabilise backward movement
        if not self.is_rotating:                                                    # If not actively rotating
            if self.angular_velocity > 0:
                self.apply_torque(-self.turn_speed * dt * self.stabiliser_str)      # Stabilise clockwise rotation
            elif self.angular_velocity < 0:
                self.apply_torque(self.turn_speed * dt * self.stabiliser_str)       # Stabilise counterclockwise rotation


    def avoid_asteroids(self, dt):
        for asteroid in self.asteroids:                                                     # Loop through nearby asteroids
            distance_to_asteroid = self.position.distance_to(asteroid.position)             # Calculate distance to each asteroid
            if distance_to_asteroid < 150:                                                  # If asteroid is within avoidance range
                direction_away = (self.position - asteroid.position).normalize()            # Get direction away from the asteroid
                angle_away = self.forward_direction.angle_to(direction_away)                # Calculate angle to turn away
                max_torque = self.turn_speed * dt                                           # Calculate max torque for turning
                torque = max(-max_torque, min(max_torque, (angle_away / 180) * max_torque)) # Apply limited torque to turn
                self.apply_torque(torque)                                                   # Apply torque to avoid asteroid
                self.is_rotating = True                                                     # Mark alien as rotating to avoid
                self.move(-self.move_speed * dt)                                            # Move backward to increase distance
                self.is_moving_forward = True                                               # Mark alien as moving backward


    def move_towards_player(self, dt):
        direction_to_player = (self.target.position - self.position).normalize()  # Direction vector from alien to player
        angle_to_player = self.forward_direction.angle_to(direction_to_player)    # Angle between alien's forward direction and player
        max_torque = self.turn_speed * dt                                         # Max torque applied for turning based on delta time
        torque = max(-max_torque, min(max_torque, (angle_to_player / 180) * max_torque))  # Clamp torque within the max range
        self.apply_torque(torque)                                                 # Apply the calculated torque to the alien ship
        self.is_rotating = True                                                   # Flag to indicate the alien is rotating towards the player
        if self.velocity.length() < self.max_speed:                               # Move forward if velocity is below max speed
            self.move(self.move_speed * dt)                                       # Move the alien towards the player
            self.is_moving_forward = True                                         # Flag to indicate the alien is moving forward
        else:
            self.is_moving_forward = False                                        # Alien is at max speed, no further acceleration

    def move(self, force_magnitude):
        force = self.forward_direction * force_magnitude                    # Calculate force in the forward direction
        self.velocity += force                                              # Apply the force to the ship's velocity
        right = self.right_direction * self.radius / 1.5                    # Calculate the right direction for visual effect
        b = self.position - self.forward_direction * self.radius - right    # Left trail position for visual effect
        c = self.position - self.forward_direction * self.radius + right    # Right trail position for visual effect
        FloatingText(b.x, b.y, "^", self.color, 50)                         # Create floating text visual effect on the left side
        FloatingText(c.x, c.y, "^", self.color, 50)                        # Create floating text visual effect on the right side


    def shoot_if_in_range(self):
        distance_to_player = self.position.distance_to(self.target.position)                # Calculate the distance to the player
        if distance_to_player < self.shooting_range and self.timer <= 0:                    # Check if player is within shooting range and cooldown is over
            self.shoot_at(self.target)                                                      # Shoot at the player if conditions are met
        for asteroid in self.asteroids:                                                     # Loop through nearby asteroids
            distance_to_asteroid = self.position.distance_to(asteroid.position)             # Calculate distance to each asteroid
            if distance_to_asteroid < self.shooting_range and self.timer <= 0:              # Check if asteroid is within range and cooldown is over
                self.shoot_at(asteroid)                                                     # Shoot at the asteroid if conditions are met

    def shoot_at(self, target):
        direction_to_target = (target.position - self.position).normalize()                 # Calculate the normalized direction to the target
        angle_diff = self.forward_direction.angle_to(direction_to_target)                   # Calculate the angle difference to the target
        if abs(angle_diff) < 30:                                                            # Check if target is within a 30-degree arc in front
            shot_position = self.position + self.forward_direction * (self.radius + 10)     # Position the shot in front of the alien ship
            new_shot = Shot(shot_position.x, shot_position.y, SHOT_RADIUS, self)            # Create and fire a new shot
            new_shot.velocity = ALIEN_SHOT_SPEED * self.forward_direction + self.velocity   # Set shot velocity based on alien's forward direction
            if new_shot.velocity.length() < PLAYER_SHOT_SPEED:                              # Ensure shot has a minimum speed
                new_shot.velocity.scale_to_length(PLAYER_SHOT_SPEED)                        # Adjust shot velocity to at least PLAYER_SHOT_SPEED
            FloatingText(shot_position.x, shot_position.y, "ø", (ALIEN_COLOR), 40)          # Create a visual effect for the shot
            self.timer = ALIEN_SHOOT_COOLDOWN                                               # Reset shooting cooldown timer

    def death(self):
        scream = random.choice(alien_screams)                                       # Choose a random alien scream
        FloatingText(self.position.x, self.position.y, scream, ALIEN_COLOR, 3000)   # Display scream as floating text
        explosion = Explosion(self.position.x, self.position.y, 7)                  # Create an explosion at the alien's position
        if random.random() < LOOT_DROP_CHANCE:                                      # Spawn loot based on a random chance
            new_loot = LootSpawner(self, self.position.x, self.position.y, 20, 1)   # Spawn loot with a 1s delay
        self.kill()                                                                 # Remove the alien from the game
    
    def shrapnel_obj(self, mass):
        """ AlienShip's custom shrapnel generation, including death logic. """
        if self.destroyed:                                                          # If the alien is already destroyed, skip further actions
            return
        self.kill()                                                                 # Remove the alien from the game
        self.destroyed = True                                                       # Mark the alien as destroyed to prevent further calls
        self.death()                                                                # Trigger alien death (scream, explosion, loot)
        self.create_shrapnel(mass)                                                  # Generate shrapnel based on the given mass
