import pygame
from circleshape import CircleShape

class FloatingText(CircleShape):
    def __init__(self, x, y, radius, message, RGB, duration):
        # Initialize the base CircleShape
        super().__init__(x, y, radius)
        self.message = message
        self.duration = duration  # Duration in milliseconds
        self.RGB = RGB
        self.start_time = pygame.time.get_ticks()
        # Create a font and render the text surface
        self.font = pygame.font.Font(None, 34)
        self.text_surface = self.font.render(self.message, True, RGB)

    def update(self, dt):
        # Check if the duration has elapsed
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

    def draw(self, screen):
        # Center the text and draw it on the screen
        text_rect = self.text_surface.get_rect(center=(self.position.x, self.position.y))
        screen.blit(self.text_surface, text_rect)

    def collision(self, other):
        # Floating text does not interact with other objects
        pass
