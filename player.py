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
        self.friction = 0.99  # Linear friction factor (tweak as needed)
        self.angular_friction = 0.99  # Rotational friction factor (tweak as needed)
        self.speed = self.velocity.length()
        self.is_player = True
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.move_speed = PLAYER_SPEED
        self.turn_speed = PLAYER_TURN_SPEED
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        # Stabilisers attributes
        self.stabilisers = False  # Set to True to enable stabilisers
        self.stabiliser_strength = 0.7  # Strength of stabilisation (tweak this)
        self.forward_velocity = self.velocity.dot(self.forward_direction)
        self.shot_damage = PLAYER_SHOT_DMG
        
    def triangle(self):
        # Calculate the points of the triangle representing the player
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5 
        a = self.position + forward * self.radius  # Tip of the triangle
        b = self.position - forward * self.radius - right  # Left corner
        c = self.position - forward * self.radius + right  # Right corner
        return [a, b, c]

    def draw(self, screen):
        # Draw the player as a triangle
        points = self.triangle()
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)

    def update(self, dt):
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation) # setting forward direction 
        self.velocity *= self.friction  # Apply linear friction
        self.angular_velocity *= self.angular_friction  # Apply rotational friction
        self.forward_velocity = self.velocity.dot(self.forward_direction)
        self.position += self.velocity * dt  # Update position based on velocity
        self.rotation += self.angular_velocity * dt  # Update rotation based on angular velocity
        self.wrap_around_screen()         # Wrap around screen edge detection
        self.timer -= dt         # Decrease the shooting timer 
        self.time += dt
        
        # Handle player input and update player state
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.apply_torque(-self.turn_speed * dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.apply_torque(self.turn_speed_SPEED * dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-self.move_speed * dt)#down
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(self.move_speed * dt) # up
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()

        if self.stabilisers:    # Apply stabilisers for each direction if active
            if not (keys[pygame.K_w] or keys[pygame.K_UP]):
                if self.forward_velocity > 0:
                    self.move(-self.move_speed * dt * self.stabiliser_strength) #down
            if not (keys[pygame.K_s] or keys[pygame.K_DOWN]):
                if self.forward_velocity < 0:
                    self.move(self.move_speed * dt * self.stabiliser_strength) # move up
            if not (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                if self.angular_velocity < 0:
                    self.apply_torque(self.turn_speed_SPEED * dt * self.stabiliser_strength) #right
            if not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                if self.angular_velocity > 0:          
                    self.apply_torque(-self.turn_speed_SPEED * dt * self.stabiliser_strength) #left

        if self.health <= 0:
            self.player_death()

    def move(self, force_magnitude):
        # Move the player in the direction they are facing
        self.forward_direction
        force = self.forward_direction * force_magnitude
        self.velocity += force  # Apply the force to velocity
        # Create visual effect when moving
        RGB = (255, 0, 0)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        b = self.position - self.forward_direction * self.radius - right
        c = self.position - self.forward_direction * self.radius + right
        FloatingText(b.x, b.y, "^", RGB, 50)
        FloatingText(c.x, c.y, "^", RGB, 50)

    def apply_force(self, force):
        self.velocity += force

    def apply_torque(self, torque):
        # Change the angular velocity by applying a torque (for rotation)
        self.angular_velocity += torque

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
        new_shot.velocity = PLAYER_SHOT_SPEED * self.forward_direction + self.velocity
        if new_shot.velocity.length() < PLAYER_SHOT_SPEED:
            new_shot.velocity.scale_to_length(PLAYER_SHOT_SPEED) 
        FloatingText(shot_position.x, shot_position.y, "ø", (255, 0, 0), 40) # Create visual effect when shooting
        self.timer = self.shot_cooldown # Reset the shooting timer

    def player_death(self):
        scream = random.choice(player_death_screams)
        FloatingText(self.position.x, self.position.y, scream, (250, 200, 100), 2000)
        player_explosion = Explosion(self.position.x, self.position.y, 400)
        self.shrapnel_obj(self.radius, (255, 10, 15))

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

