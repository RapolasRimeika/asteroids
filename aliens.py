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

        Attributes:
            isalien (bool): Marks the object as an alien ship.
            color (tuple): The color of the alien ship, used for rendering.
            move_speed (float): The speed at which the alien moves.
            turn_speed (float): The speed at which the alien turns.
            shooting_range (float): The maximum distance from which the alien can shoot at the player or asteroids.
            shot_damage (int): The amount of damage the alien's shots deal to targets.
            health (int): The current health of the alien ship.
            max_speed (float): The maximum linear speed the alien can achieve.
            max_ang_velocity (float): The maximum angular velocity for turning.
            target (Player): A reference to the player object, which the alien targets.
            asteroids (list): A list of asteroid objects, used for avoiding collisions.
            timer (float): A cooldown timer for controlling the rate at which the alien fires shots.
            angular_velocity (float): The current angular velocity (turn speed) of the alien.
            forward_velocity (float): The current forward velocity of the alien.
            right_velocity (float): The current rightward velocity of the alien.
            score (int): The score value awarded for destroying the alien.
            forward_direction (Vector2): The vector representing the direction the alien is facing.
            right_direction (Vector2): The vector perpendicular to the forward direction.
            stabilisers (bool): A flag indicating whether stabilizers are enabled to smooth movements.
            stabiliser_str (float): The strength of the stabilizers in counteracting movement and rotation.

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
        self.right_velocity = 0                                 # Initial rightward velocity of the alien ship        self.score = 0
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.right_direction = self.forward_direction.rotate(90)
        self.stabilisers = True                                 # Enable stabilisers
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
        # Draw the alien ship as a triangle
        points = self.triangle()
        pygame.draw.polygon(screen, self.color, points)

    def update(self, dt):
        #if self.health <= 0:                                # Check if the alien's health is zero or below
         #   self.death()                                    # Call death method if the alien is dead
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
        # Apply stabilisers if enabled
        if self.stabilisers:                                                # Check if stabilisers are enabled
            self.stabilise(dt)                                              # Apply stabilisation logic to smooth movements

    def stabilise(self, dt):
        """
        Applies stabilisers to reduce small movements and rotational drifts if enabled.
        Args: dt (float): The time delta for frame-based updates.
        """
        # Apply thresholds to stop small movements
        
        if abs(self.forward_velocity) < self.velocity_threshold:
            self.forward_velocity = 0
        if abs(self.right_velocity) < self.velocity_threshold:
            self.right_velocity = 0
        if abs(self.angular_velocity) < self.velocity_threshold:
            self.angular_velocity = 0

        # Apply force to stabilise forward movement if not actively moving
        if not self.is_moving_forward:
            if self.forward_velocity > 0:
                self.move(-self.move_speed * dt * self.stabiliser_str)
            elif self.forward_velocity < 0:
                self.move(self.move_speed * dt * self.stabiliser_str)

        # Apply torque to stabilise rotation if not actively rotating
        if not self.is_rotating:
            if self.angular_velocity > 0:
                self.apply_torque(-self.turn_speed * dt * self.stabiliser_str)
            elif self.angular_velocity < 0:
                self.apply_torque(self.turn_speed * dt * self.stabiliser_str)


    def avoid_asteroids(self, dt):
        # Check for nearby asteroids and adjust movement to avoid them
        for asteroid in self.asteroids:
            distance_to_asteroid = self.position.distance_to(asteroid.position)
            if distance_to_asteroid < 150:  # Arbitrary distance to start avoiding
                # Calculate direction away from the asteroid
                direction_away = (self.position - asteroid.position).normalize()
                angle_away = self.forward_direction.angle_to(direction_away)

                # Apply torque to turn away from the asteroid
                max_torque = self.turn_speed * dt
                torque = max(-max_torque, min(max_torque, (angle_away / 180) * max_torque))
                self.apply_torque(torque)
                self.is_rotating = True  # Alien is rotating to avoid asteroid

                # Move backward to avoid collision
                self.move(-self.move_speed * dt)
                self.is_moving_forward = True  # Alien is moving (backward in this case)

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
        # Move the alien ship in the direction it is facing
        force = self.forward_direction * force_magnitude
        self.velocity += force  # Apply the force to velocity
        # Optionally, create a visual effect when moving
        right = self.right_direction * self.radius / 1.5
        b = self.position - self.forward_direction * self.radius - right
        c = self.position - self.forward_direction * self.radius + right
        FloatingText(b.x, b.y, "^", ALIEN_COLOR, 50)
        FloatingText(c.x, c.y, "^", ALIEN_COLOR, 50)

    def apply_torque(self, torque):
        # Change the angular velocity by applying a torque (for rotation)
        self.angular_velocity += torque

    def shoot_if_in_range(self):
        # Shoot at the player if within range and if alien is facing the player
        distance_to_player = self.position.distance_to(self.target.position)
        if distance_to_player < self.shooting_range and self.timer <= 0:
            self.shoot_at(self.target)

        # Shoot at nearby asteroids if in range
        for asteroid in self.asteroids:
            distance_to_asteroid = self.position.distance_to(asteroid.position)
            if distance_to_asteroid < self.shooting_range and self.timer <= 0:
                self.shoot_at(asteroid)

    def shoot_at(self, target):
        # Only shoot if the alien ship is facing the target
        direction_to_target = (target.position - self.position).normalize()
        angle_diff = self.forward_direction.angle_to(direction_to_target)

        if abs(angle_diff) < 30:  # Check if the target is within the 30-degree arc in front
            shot_position = self.position + self.forward_direction * (self.radius + 10)
            new_shot = Shot(shot_position.x, shot_position.y, SHOT_RADIUS, self)    # Create and fire a shot
            new_shot.velocity = ALIEN_SHOT_SPEED * self.forward_direction + self.velocity
            if new_shot.velocity.length() < PLAYER_SHOT_SPEED:
                new_shot.velocity.scale_to_length(PLAYER_SHOT_SPEED)
            FloatingText(shot_position.x, shot_position.y, "ø", (ALIEN_COLOR), 40)  # Create visual effect
            self.timer = ALIEN_SHOOT_COOLDOWN                                       # Reset the shooting timer



    def death(self):
        scream = random.choice(alien_screams)
        FloatingText(self.position.x, self.position.y, scream, ALIEN_COLOR, 3000)
        explosion = Explosion(self.position.x, self.position.y, 7)
        if random.random() < LOOT_DROP_CHANCE:  # Only spawn loot some percentage of the time
            new_loot = LootSpawner(self, self.position.x, self.position.y, 20, 1)  # Delay of 1s
        self.kill()
    
    def shrapnel_obj(self, mass):
        """
        AlienShip's custom shrapnel generation, including death logic.
        """
        if self.destroyed:
            return
        self.kill()
        self.destroyed = True
        self.death()                                                     # Call alien's death method
        self.create_shrapnel(mass)   