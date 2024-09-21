from constants import *
from circleshape import CircleShape
from shot import Shot
from floating_text import FloatingText
import pygame


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0 #initialize rotation attribute
        self.timer = 0
        

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5 
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        points = self.triangle()
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)
      
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move((dt))
        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()
        
        self.timer -= dt

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        RGB = (255, 0, 0)
        right = right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        new_message = FloatingText(b[0], b[1], 1,"^", RGB, 50)
        new_message = FloatingText(c[0], c[1], 1, "^", RGB, 50)

    def shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        a = self.position + forward * self.radius
        radius = SHOT_RADIUS
        new_shot = Shot(a[0], a[1], radius)
        new_shot.velocity = PLAYER_SHOT_SPEED * pygame.Vector2(0, 1).rotate(self.rotation)
        RGB = (255, 0, 0)
        new_message = FloatingText(a[0], a[1], 1, "ø", RGB, 40)
        self.timer = PLAYER_SHOOT_COOLDOWN