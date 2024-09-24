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
        
        self.forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        
        # Stabilisers attributes
        self.stabilisers = True  # Set to True to enable stabilisers
        self.stabiliser_strength = 0.7  # Strength of stabilisation (tweak this)
        self.forward_velocity = self.velocity.dot(self.forward_direction)
        
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
        if self.health <= 0:
            self.player_death()
        
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
            self.apply_torque(-PLAYER_TURN_SPEED * dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.apply_torque(PLAYER_TURN_SPEED * dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-self.move_speed * dt)#down
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(self.move_speed * dt) # up
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()

        # Apply stabilisers for each direction if active
        if self.stabilisers:
            if not (keys[pygame.K_w] or keys[pygame.K_UP]):
                self.stabilise_forward(dt)
            if not (keys[pygame.K_s] or keys[pygame.K_DOWN]):
                self.stabilise_backwards(dt)
            if not (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                self.stabilise_rotation_left(dt)
            if not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                self.stabilise_rotation_right(dt)

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

    def stabilise_forward(self, dt):
        """Apply force to stop forward velocity."""
        if self.forward_velocity > 0:
            self.move(-self.move_speed * dt * self.stabiliser_strength) #down
    def stabilise_backwards(self, dt):
        """Apply force to stop backward velocity."""
        if self.forward_velocity < 0:
            self.move(self.move_speed * dt * self.stabiliser_strength) # move up

    def stabilise_rotation_left(self, dt):
        """Apply torque to stop leftward rotation."""
        # If rotating left (angular velocity < 0), apply torque to stabilize
        if self.angular_velocity < 0:
            self.apply_torque(PLAYER_TURN_SPEED * dt * self.stabiliser_strength) #right

    def stabilise_rotation_right(self, dt):
        """Apply torque to stop rightward rotation."""
        # If rotating right (angular velocity > 0), apply torque to stabilize
        if self.angular_velocity > 0:          
            self.apply_torque(-PLAYER_TURN_SPEED * dt * self.stabiliser_strength) #left

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
        shot_position = self.position + self.forward_direction * (self.radius + 10)
        new_shot = Shot((shot_position.x), (shot_position.y), SHOT_RADIUS, self) # adding a modifyier to y so that the new shot wouldn't collide with the player
        
        # Incorporate the player's velocity into the shot's velocity
        new_shot.velocity = PLAYER_SHOT_SPEED * self.forward_direction + self.velocity
        if new_shot.velocity.length() < PLAYER_SHOT_SPEED:
            new_shot.velocity.scale_to_length(PLAYER_SHOT_SPEED) 
        # Create visual effect when shooting
        RGB = (255, 0, 0)
        FloatingText(shot_position.x, shot_position.y, "ø", RGB, 40)

        # Reset the shooting timer
        self.timer = self.shot_cooldown

    def score_points(self, points):
        # Points update function
        self.score += points

    def get_score(self):
        # Point getter function
        return self.score

    def get_time(self):
        # Get time player has been playing
        return round((self.time), 1)

    def player_death(self):
        RGB = (250, 200, 100)
        scream = random.choice(player_death_screams)
        FloatingText(self.position.x, self.position.y, scream, RGB, 2000)
        self.shrapnel_obj(self.radius, (255, 0, 0))
        explosion = Explosion(self.position.x, self.position.y, 400)
        self.kill()

    def bounce(self, other):
        super().bounce(other)

    def destroy_asteroid(self, value):
        self.asteroids_destroyed += value

