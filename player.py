import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot
from floating_text import FloatingText


class Player(CircleShape):
    def __init__(self, x, y):
        # Initialize the player with position and radius
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # Initialize rotation angle
        self.timer = 0  # Timer for shooting cooldown
        self.score = 0 # Score value initialize
        self.time = 0

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
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()

        # Decrease the shooting timer   
        self.timer -= dt

        self.time += dt

    def rotate(self, dt):
        # Rotate the player by adjusting the rotation angle
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        # Move the player in the direction they are facing
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        # Create visual effect when moving
        RGB = (255, 0, 0)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        FloatingText(b.x, b.y, 1, "^", RGB, 50)
        FloatingText(c.x, c.y, 1, "^", RGB, 50)
        # Wrap around screen edges
        self.wrap_around_screen()

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
        shot_position = self.position + forward * self.radius
        new_shot = Shot(shot_position.x, shot_position.y, SHOT_RADIUS)
        new_shot.velocity = PLAYER_SHOT_SPEED * forward
        # Create visual effect when shooting
        RGB = (255, 0, 0)
        FloatingText(shot_position.x, shot_position.y, 1, "ø", RGB, 40)
        # Reset the shooting timer
        self.timer = PLAYER_SHOOT_COOLDOWN

    def score_points(self, points): 
        # Points update function 
        self.score += points

    def get_score(self):
        # Point getter function
        return self.score
    
    def get_time(self):
        # Get time player playing
        return round((self.time), 1)