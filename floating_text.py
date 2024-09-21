import pygame
from circleshape import CircleShape

class FloatingText(CircleShape):
    def __init__(self, x, y, radius, message):
        super().__init__(x, y, radius)
        self.message = message
        self.duration = duration = 1000
        self.start_time = pygame.time.get_ticks()
        self.font = font = pygame.font.Font(None, 24)
        self.text_surface = self.font.render(self.message, True, (255, 0, 0))

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

    def draw(self, screen):
            screen.blit(self.text_surface, (self.position[0], self.position[1]))

    def collision(self, other):
        pass