import pygame

class FloatingText(pygame.sprite.Sprite):
    containers = []  # This will be set to the relevant sprite groups from the main loop

    def __init__(self, x, y, message, RGB, duration):
        super().__init__(self.containers)  # Automatically add to all specified sprite groups
        self.x = x
        self.y = y
        self.message = message
        self.duration = duration  # Duration in milliseconds
        self.RGB = RGB
        self.start_time = pygame.time.get_ticks()
        # Create a font and render the text surface
        self.font = pygame.font.Font(None, 34)
        self.text_surface = self.font.render(self.message, True, self.RGB)

    def update(self, dt):
        # Check if the duration has elapsed
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()  # Remove the floating text after its duration

    def draw(self, screen):
        # Draw the text on the screen at its (x, y) position
        text_rect = self.text_surface.get_rect(center=(self.x, self.y))
        screen.blit(self.text_surface, text_rect)
