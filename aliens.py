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
    def __init__(self, x, y, ALIEN_RADIUS, player, asteroids):
        super().__init__(x, y, ALIEN_RADIUS)  # Set radius to 25
        self.player = player  # Reference to the player object
        self.asteroids = asteroids  # List of asteroid objects
        self.timer = 0  # Shooting cooldown timer
        self.shooting_range = 300  # Max range to shoot at player or asteroids
        self.color = (0, 255, 0)  # Set the alien ship color to green
        self.health = self.radius * 2
        self.score = 0
        self.isalien = True

    def triangle(self):
        # Calculate the points of the triangle representing the alien ship
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius  # Tip of the triangle
        b = self.position - forward * self.radius - right  # Left corner
        c = self.position - forward * self.radius + right  # Right corner
        return [a, b, c]

    def draw(self, screen):
        # Draw the alien ship as a triangle
        points = self.triangle()
        pygame.draw.polygon(screen, self.color, points, 2)

    def update(self, dt):
        if self.health <= 0:
            self.death(dt)

        # Move the alien ship based on its AI behavior
        self.avoid_asteroids(dt)
        self.move_towards_player(dt)

        # Shoot at the player if within range, or nearby asteroids
        self.shoot_if_in_range()

        # Apply linear and angular friction to slow down
        self.velocity *= self.friction
        self.angular_velocity *= self.angular_friction

        # Update position and rotation based on velocities
        self.position += self.velocity * dt
        self.rotation += self.angular_velocity * dt
        self.rotation %= 360  # Keep the rotation angle between 0 and 360 degrees

        # Wrap around screen edges
        self.wrap_around_screen()

        # Decrease shooting cooldown timer
        self.timer -= dt

    def avoid_asteroids(self, dt):
        # Check for nearby asteroids and move away if too close
        for asteroid in self.asteroids:
            distance_to_asteroid = self.position.distance_to(asteroid.position)
            if distance_to_asteroid < 60:  # Arbitrary distance to avoid asteroids
                direction_away = self.position - asteroid.position
                direction_away.normalize_ip()  # Normalize to get the direction
                self.apply_force(direction_away * ALIEN_AVOID_FORCE * dt)  # Move away from asteroid

    def move_towards_player(self, dt):
        # Move towards the player
        direction_to_player = self.player.position - self.position
        direction_to_player.normalize_ip()  # Normalize to get direction
        self.apply_force(direction_to_player * ALIEN_SPEED * dt)  # Move towards player

        # Rotate to face the player
        angle_to_player = atan2(-direction_to_player.y, direction_to_player.x)
        self.rotation = degrees(angle_to_player) + 90  # Adjust for vertical sprite orientation

    def shoot_if_in_range(self):
        # Shoot at the player if within range and if alien is facing the player
        distance_to_player = self.position.distance_to(self.player.position)
        if distance_to_player < self.shooting_range and self.timer <= 0:
            self.shoot_at(self.player)

        # Shoot at nearby asteroids if in range
        for asteroid in self.asteroids:
            distance_to_asteroid = self.position.distance_to(asteroid.position)
            if distance_to_asteroid < self.shooting_range and self.timer <= 0:
                self.shoot_at(asteroid)

    def shoot_at(self, target):
        # Only shoot if the alien ship is facing the target
        direction_to_target = (target.position - self.position).normalize()
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        angle_diff = forward.angle_to(direction_to_target)

        if abs(angle_diff) < 30:  # Check if the target is within the 30-degree arc in front
            shot_position = self.position + forward * (self.radius + 10)
            # Create and fire a shot
            new_shot = Shot(shot_position.x, shot_position.y, SHOT_RADIUS, self)
            new_shot.velocity = ALIEN_SHOT_SPEED * forward + self.velocity
            # Reset the shooting timer (alien can't shoot too frequently)
            self.timer = ALIEN_SHOOT_COOLDOWN

    def wrap_around_screen(self):
        # Wrap the alien to the opposite side if it moves off-screen
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def death(self, dt):
        RGB = (250, 200, 100)
        scream = random.choice(alien_screams)
        FloatingText(self.position.x, self.position.y, scream, RGB, 3000)
        self.shrapnel_obj(self.radius)
        explosion = Explosion(self.position.x, self.position.y, (self.radius * 7))
        # Spawn loot upon alien death after delay
        if random.random() < LOOT_DROP_CHANCE:  # Only spawn loot some percentage of the time
            new_loot = LootSpawner(self, self.position.x, self.position.y, 20, 1)  # Delay of 1s
        self.kill()