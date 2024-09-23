import pygame
import random
from constants import *
from circleshape import CircleShape
from floating_text import FloatingText
from circleshape import Shrapnel

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        # Initialize the asteroid with position and radius
        super().__init__(x, y, radius)
       
    def draw(self, screen):
        # Draw the asteroid as a white circle
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self, dt):
        # Update position based on velocity and time delta
        self.position += self.velocity * dt
        if self.health == (self.max_health / 2):
            self.split

    def split(self):
        # Remove the current asteroid
        self.kill()
        self.shrapnel_asteroid(20)
        RGB = (255, 0, 150)
        explosion_list = ["CRASH!", "BLAM!", "BANG!", "BOOMSHAK!", "THWACK!", "SMASH!", "THOOM!", "ZAP!", "BLAST!", "KA-BLAST!", "KABLAM!", "WHOOSH!", "CRACK!", "THUD!", "WHAM!"]
        explosion =random.choice(explosion_list)
        FloatingText(self.position.x, self.position.y, (f"{explosion}"), RGB, 500)
        
         # Stop splitting if the asteroid is at minimum size
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.shrapnel_obj((self.radius))
            return
        # Create two smaller asteroids with new velocities
        random_angle = random.uniform(20, 50)
        velocity_a = self.velocity.rotate(random_angle) * 1.2
        velocity_b = self.velocity.rotate(-random_angle) * 1.2
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        # Spawn the new asteroids
        Asteroid(self.position.x, self.position.y, new_radius).velocity = velocity_a
        Asteroid(self.position.x, self.position.y, new_radius).velocity = velocity_b

    def shrapnel_obj(self, mass, RGB=(150, 150, 150)):
        while mass > 1:
            random_angle = random.uniform(0, 360)
            velocity_a = self.velocity.rotate(random_angle) * random.uniform(0.5, 2.5)
            new_radius = random.uniform(2, 5)
            # Spawn shrapnel
            shrapnel_piece = Shrapnel(self.position.x, self.position.y, new_radius, RGB)
            shrapnel_piece.velocity = velocity_a
            mass -= new_radius