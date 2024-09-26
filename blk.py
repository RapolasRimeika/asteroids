import pygame

class BLK(pygame.sprite.Sprite):
    def __init__(self):
        # Automatically add the Explosion to the appropriate groups
        super().__init__(self.containers if hasattr(self, "containers") else None)
        self.is_explosion = True
        # Set position and explosion properties
        self.far_radius = 1500
        self.position = pygame.Vector2(100, 100)
        self.health = 1000000000000000
     
        self.near = self.far_radius / 4
        self.mid_radius = self.far_radius / 2
       # self.far_radius = far_radius
        self.color = (150, 120, 160)
        self.radius = 100  



    def update(self, dt):
        """ Placeholder for updates if needed later """
        if self.health < 5000: self.health += 1000 

    def collision(self, other, bounce=True):
        print(f"Explosion colliding with {other}")
        distance = self.position.distance_to(other.position)
        self.radius = 100
        if distance <= self.far_radius + other.radius: #whitin range
            if distance <= self.radius:
                other.kill()

            if distance <= self.near: #close range
                strength = - 1
                self.calculate_force(other, strength)
            elif distance <= self.mid_radius: #mid range
                strength = -0.1
                self.calculate_force(other, strength) 
            else:
                strength = -0.03
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

    
    def apply_force(self, other):
        pass