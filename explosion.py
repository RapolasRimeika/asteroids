import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, far_radius):
        # Automatically add the Explosion to the appropriate groups
        super().__init__(self.containers if hasattr(self, "containers") else None)
        self.is_explosion = True
        # Set position and explosion properties
        self.position = pygame.Vector2(x, y)
        self.near = far_radius / 3
        self.mid_radius = far_radius / 1.5
        self.far_radius = far_radius
        self.color = (189, 12, 16)
        self.radius = 1  # Explosion's own radius for collision detection

    def update(self, dt):
        """ Placeholder for updates if needed later """
        pass

    def collision(self, other, bounce=True):
        print(f"Explosion colliding with {other}")
        distance = self.position.distance_to(other.position)

        if distance <= self.far_radius + other.radius: #whitin range
            if distance <= self.near: #close range
                strength = 4
                self.calculate_force(other, strength)
            elif distance <= self.mid_radius: #mid range
                strength = 2
                self.calculate_force(other, strength) 
            else:
                strength = 1
                self.calculate_force(other, strength)

        
        
    def calculate_force(self, other, strength):
        """ Apply force to the object based on proximity """
        explosion_vector = other.position - self.position
        if explosion_vector.length() > 0:
            explosion_vector.normalize_ip()
        force = explosion_vector * strength * 100  # Scale force
        other.apply_force(force)

    def draw(self, screen):
        """ Visualize the explosion radius on the screen """
        for radius in [self.near, self.mid_radius, self.far_radius]:
            pygame.draw.circle(screen, self.color, (int(self.position.x +1 ), int(self.position.y + 1)), int(radius), 2)
            self.kill()  # Remove the explosion after applying force
    
    def apply_force(self, other):
        pass