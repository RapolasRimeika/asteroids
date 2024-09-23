import pygame
import random
from constants import *
from circleshape import CircleShape
from shot import Shot
from floating_text import FloatingText
from circleshape import Shrapnel

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
        # Handle player input and update player state
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.apply_torque(-PLAYER_TURN_SPEED * dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.apply_torque(PLAYER_TURN_SPEED * dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.apply_force(-PLAYER_SPEED * dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.apply_force(PLAYER_SPEED * dt)
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()

        # Apply friction to slow down movement and rotation over time
        self.velocity *= self.friction  # Apply linear friction
        self.angular_velocity *= self.angular_friction  # Apply rotational friction

        # Update position and rotation based on velocities
        self.position += self.velocity * dt  # Update position based on velocity
        self.rotation += self.angular_velocity * dt  # Update rotation based on angular velocity

        # Wrap around screen edges
        self.wrap_around_screen()

        # Decrease the shooting timer   
        self.timer -= dt
        self.time += dt

        if self.health <= 0:
            self.player_death()

    def apply_force(self, force_magnitude):
        # Move the player in the direction they are facing
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        force = forward * force_magnitude
        self.velocity += force  # Apply the force to velocity
        # Create visual effect when moving
        RGB = (255, 0, 0)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        FloatingText(b.x, b.y, "^", RGB, 50)
        FloatingText(c.x, c.y, "^", RGB, 50)

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
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot_position = self.position + forward * (self.radius + 10)
        
        new_shot = Shot(shot_position.x, shot_position.y, SHOT_RADIUS)
        new_shot.velocity = PLAYER_SHOT_SPEED * forward
        
        # Create visual effect when shooting
        RGB = (255, 0, 0)
        FloatingText(shot_position.x, shot_position.y, "ø", RGB, 40)

        # Reset the shooting timer
        self.timer = PLAYER_SHOOT_COOLDOWN

    def score_points(self, points):
        # Points update function
        self.score += points

    def get_score(self):
        # Point getter function
        return self.score

    def get_time(self):
        # Get time player has been playing
        return round((self.time), 1)

def collision(self, other, bounce=True):
    # Check for collision with another CircleShape
    distance = self.position.distance_to(other.position)
    if self.radius + other.radius > distance:
        # Calculate damage based on the other object's radius and speed
        impact_force = other.radius * other.velocity.length()
        self.health -= impact_force
        
        # Log health and damage taken for debugging purposes
        print(f"Player health: {self.health}, Damage taken: {impact_force}")

        # Bounce if enabled
        if bounce:
            self.bounce(other)
        
        # Check if player is dead
        if self.health <= 0:
            self.player_death()

        return True
    return False

    def player_death(self):
        RGB = (250, 200, 100)
        collision_screams = [
            "ARGHHH!", "No! No! No!  NOOOOOOOOO!!!", "NO!", 
            "We're crashing!", "Eject!", "Tell her I love her!", 
            "Beam me out of here!"
        ]
        scream = random.choice(collision_screams)
        FloatingText(self.position.x, self.position.y, scream, RGB, 2000)
        self.shrapnel()
        self.kill()

    def bounce(self, other):
        super().bounce(other)

    def shrapnel(self):
        RGB = (255, 0, 0)
        FloatingText(self.position.x, self.position.y, "O", RGB, 40)
        mass = PLAYER_RADIUS
        while mass > 1:
            random_angle = random.uniform(90, 270)
            velocity_a = self.velocity.rotate(random_angle) * random.uniform(0.5, 1.5)
            new_radius = random.uniform(1, 5)
            # Spawn shrapnel
            shrapnel_piece = Shrapnel(self.position.x, self.position.y, new_radius)
            shrapnel_piece.velocity = velocity_a
            mass -= new_radius

    def destroy_asteroid(self, value):
        self.asteroids_destroyed += value

        RGB = (255, 0, 150)
        asteroid_down_messages = [
            "Asteroid shot down!", "Target destroyed!", "Direct hit!", 
            "Asteroid obliterated!", "Hit confirmed!", "Asteroid vaporized!", 
            "Threat eliminated!", "Asteroid shattered!", "Bullseye!", 
            "Rock smashed!", "Target disintegrated!", "Asteroid annihilated!", 
            "Strike successful!"
        ]
        asteroid_down_message = random.choice(asteroid_down_messages)
        FloatingText(120, 40, (f"{asteroid_down_message}"), RGB, 500)
