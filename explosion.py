import pygame
from constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, multiplier=1):
        # Automatically add the Explosion to the appropriate groups
        super().__init__(self.containers if hasattr(self, "containers") else None)
        self.is_explosion = True
        # Set position and explosion properties
        self.position = pygame.Vector2(x, y)
        self.radius =       EXPLOSION_INITIAL_RADIUS * multiplier # Explosion's own radius for collision detection
        self.near =         EXPLOSION_NEAR_RADIUS
        self.mid_radius =   EXPLOSION_MID_RADIUS
        self.far_radius =   EXPLOSION_FAR_RADIUS
        self.color =        EXPLOSION_COLOR
        self.health = 1

    def update(self, dt):
        pass

    def collision(self, other, bounce=True):
        print(f"Explosion colliding with {other}")
        distance = self.position.distance_to(other.position)

        if distance <= self.far_radius + other.radius: #whitin range
            if distance <= self.near: #close range
                strength = EXPLOSION_NEAR_STRENGTH
                self.calculate_force(other, strength)
            elif distance <= self.mid_radius: #mid range
                strength = EXPLOSION_MID_STRENGTH
                self.calculate_force(other, strength) 
            else:
                strength = EXPLOSION_FAR_STRENGTH
                self.calculate_force(other, strength) 
        
    def calculate_force(self, other, strength):
        explosion_vector = other.position - self.position
        if explosion_vector.length() > 0:
            explosion_vector.normalize_ip()
        force = explosion_vector * strength 
        other.apply_force(force)
        self.kill()  # Remove the explosion after applying force

    def draw(self, screen):
        for radius in [self.near, self.mid_radius, self.far_radius]:
            pygame.draw.circle(screen, self.color, (int(self.position.x +1 ), int(self.position.y + 1)), int(radius), 2)
    
    def apply_force(self, other):
        pass

    def shrapnel_obj(self, mass, RGB=(150, 150, 150),):
        pass