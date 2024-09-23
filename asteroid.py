import pygame
import random
from circleshape import CircleShape
from floating_text import FloatingText
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, RGB=(150, 150, 150)):
        # Initialize the asteroid with position, radius, and color
        super().__init__(x, y, radius)
        self.color = RGB

    def update(self, dt):
        # Call the parent class's update method to handle movement and inertia
        super().update(dt)

        # When the asteroid's health drops below half, check for split
        if self.health < self.max_health / 2 and self.radius > 10:
            self.split()
        elif self.health <= 0 and self.radius <= 10:
            # If the asteroid is at its smallest size and health is depleted, produce shrapnel
            self.shrapnel_obj(self.radius)
            self.kill()

    def split(self):
        if self.radius > ASTEROID_MIN_RADIUS:
            # Split the asteroid into two smaller pieces
            new_radius = self.radius / 2

            # Create two smaller asteroids
            for _ in range(2):
                split_velocity = self.velocity.rotate(random.uniform(-30, 30)) * random.uniform(0.5, 1.5)
                smaller_asteroid = Asteroid(self.position.x, self.position.y, new_radius, self.color)
                smaller_asteroid.velocity = split_velocity

            # Floating text effect for asteroid splitting
            RGB = (255, 0, 150)
            explosion_list = ["CRASH!", "BLAM!", "BANG!", "BOOMSHAK!", "THWACK!", "SMASH!", "THOOM!", "ZAP!", "BLAST!", "KA-BLAST!", "KABLAM!", "WHOOSH!", "CRACK!", "THUD!", "WHAM!"]
            explosion =random.choice(explosion_list)
            FloatingText(self.position.x, self.position.y, (f"{explosion}"), RGB, 500)

            # Remove the original asteroid after splitting
            self.kill()
            self.shrapnel_obj(self.radius, self.color)


    def draw(self, screen):
        # Draw the asteroid as a circle outline (not filled)
        pygame.draw.circle(screen, (self.color), (int(self.position.x), int(self.position.y)), self.radius, 2)

        # Floating text effect at the asteroid's position (optional)
        FloatingText(self.position.x, self.position.y, "Asteroid", (255, 255, 255), 1)

