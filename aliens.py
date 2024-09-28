import pygame
import random
from math import atan2, degrees
from constants import *
from circleshape import CircleShape
from shot import Shot
from floating_text import FloatingText
from circleshape import Shrapnel
from text_lists import alien_screams
from loot import LootSpawner
from explosion import Explosion

class AlienShip(CircleShape):
    def __init__(self, x, y, ALIEN_RADIUS, player_target, asteroids):
        super().__init__(x, y, ALIEN_RADIUS)
        self.target = player_target                             # Reference to the player object
        self.asteroids = asteroids                              # List of asteroid objects
        self.timer = 0                                          # Shooting cooldown timer
        self.shooting_range = 600                               # Max range to shoot at player or asteroids
        self.color = (50, 190, 50)                              # Set the alien ship color to green
        self.health = self.radius * 3
        self.score = 0
        self.isalien = True
        self.shot_damage = PLAYER_SHOT_DMG
        self.angular_velocity = 0
        self.move_speed = PLAYER_SPEED * 1.5
        self.turn_speed = PLAYER_TURN_SPEED * 1.5
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.right_direction = self.forward_direction.rotate(90)
        # Stabilisers attributes
        self.stabilisers = True          # Enable stabilisers
        self.stabiliser_str = 0.5        # Strength of stabilisation (adjust as needed)
        self.forward_velocity = 0        # Initialize forward velocity
        self.right_velocity = 0          # Initialize right velocity
        self.max_speed = 300             # Define a maximum speed for the alien
        self.max_angular_velocity = 300  # Maximum angular velocity in degrees per second

    def triangle(self):  # Calculate the points of the triangle representing the alien ship
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius  # Tip of the triangle
        b = self.position - forward * self.radius - right  # Left corner
        c = self.position - forward * self.radius + right  # Right corner
        return [a, b, c]

    def draw(self, screen):
        # Draw the alien ship as a triangle
        points = self.triangle()
        pygame.draw.polygon(screen, self.color, points)

    def update(self, dt):
        if self.health <= 0:
            self.death()

        # Update the forward and right directions based on current rotation
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.right_direction = self.forward_direction.rotate(90)
        # Apply friction to linear and angular velocities
        self.velocity *= self.friction
        self.angular_velocity *= self.angular_friction
        # Calculate velocities relative to the ship's facing direction
        self.forward_velocity = self.velocity.dot(self.forward_direction)
        self.right_velocity = self.velocity.dot(self.right_direction)
        # Clamp velocities to maximum values
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.angular_velocity = max(-self.max_angular_velocity, min(self.angular_velocity, self.max_angular_velocity))
        # Update position and rotation based on velocities
        self.position += self.velocity * dt
        self.rotation += self.angular_velocity * dt
        self.rotation %= 360                # Keep the rotation angle between 0 and 360 degrees
        self.timer -= dt                    # Decrease shooting cooldown timer
        # Flags to determine if the alien is actively moving or rotating
        self.is_moving_forward = False
        self.is_rotating = False
        # Move the alien ship based on its behavior
        self.avoid_asteroids(dt)
        self.move_towards_player(dt)
        self.shoot_if_in_range()  # Shoot if within range, or nearby asteroids

        # Apply stabilisers if enabled
        if self.stabilisers:
            # Apply thresholds to stop small movements
            velocity_threshold = 0.4
            if abs(self.forward_velocity) < velocity_threshold:
                self.forward_velocity = 0
            if abs(self.right_velocity) < velocity_threshold:
                self.right_velocity = 0
            if abs(self.angular_velocity) < velocity_threshold:
                self.angular_velocity = 0

            if not self.is_moving_forward:
                if self.forward_velocity > 0:
                    self.move(-self.move_speed * dt * self.stabiliser_str)
                elif self.forward_velocity < 0:
                    self.move(self.move_speed * dt * self.stabiliser_str)

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
        # Move towards the player
        direction_to_player = (self.target.position - self.position).normalize()
        angle_to_player = self.forward_direction.angle_to(direction_to_player)

        # Apply torque to turn towards the player
        max_torque = self.turn_speed * dt
        torque = max(-max_torque, min(max_torque, (angle_to_player / 180) * max_torque))
        self.apply_torque(torque)
        self.is_rotating = True  # Alien is rotating towards the player

        # Only move if below maximum speed
        if self.velocity.length() < self.max_speed:
            self.move(self.move_speed * dt)
            self.is_moving_forward = True  # Alien is moving forward towards the player
        else:
            # If at max speed, don't apply additional force
            self.is_moving_forward = False

    def move(self, force_magnitude):
        # Move the alien ship in the direction it is facing
        force = self.forward_direction * force_magnitude
        self.velocity += force  # Apply the force to velocity
        # Optionally, create a visual effect when moving
        RGB = (0, 255, 0)
        right = self.right_direction * self.radius / 1.5
        b = self.position - self.forward_direction * self.radius - right
        c = self.position - self.forward_direction * self.radius + right
        FloatingText(b.x, b.y, "^", RGB, 50)
        FloatingText(c.x, c.y, "^", RGB, 50)

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
            new_shot = Shot(shot_position.x, shot_position.y, SHOT_RADIUS, self)  # Create and fire a shot
            new_shot.velocity = ALIEN_SHOT_SPEED * self.forward_direction + self.velocity
            if new_shot.velocity.length() < PLAYER_SHOT_SPEED:
                new_shot.velocity.scale_to_length(PLAYER_SHOT_SPEED)
            FloatingText(shot_position.x, shot_position.y, "ø", (15, 250, 15), 40) # Create visual effect
            self.timer = ALIEN_SHOOT_COOLDOWN  # Reset the shooting timer

    def death(self):
        RGB = (250, 200, 100)
        scream = random.choice(alien_screams)
        FloatingText(self.position.x, self.position.y, scream, RGB, 3000)
        self.shrapnel_obj(self.radius)
        explosion = Explosion(self.position.x, self.position.y, (self.radius * 7))
        if random.random() < LOOT_DROP_CHANCE:  # Only spawn loot some percentage of the time
            new_loot = LootSpawner(self, self.position.x, self.position.y, 20, 1)  # Delay of 1s
