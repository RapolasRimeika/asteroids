import pygame
from constants import *

class FloatingText(pygame.sprite.Sprite):
    containers = []  # This will be set to the relevant sprite groups from the main loop

    def __init__(self, x, y, message, RGB, duration, line_spacing=LINE_SPACING):
        super().__init__(self.containers)  # Automatically add to all specified sprite groups
        self.x = x
        self.y = y
        self.message = message
        self.duration = duration 
        self.RGB = RGB
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, FONT_SIZE)  # Use font size constant
        self.line_spacing = line_spacing
        self.render_lines()

    def render_lines(self):
        """Splits the message into multiple lines and creates a surface for each."""
        self.lines = self.message.split('\n')
        self.text_surfaces = []
        for line in self.lines:
            text_surface = self.font.render(line, True, self.RGB)
            self.text_surfaces.append(text_surface)

    def update(self, dt):
        # Check if the duration has elapsed
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()  # Remove the floating text after its duration

    def draw(self, screen):
        """Draw each line with appropriate line spacing."""
        for i, text_surface in enumerate(self.text_surfaces):
            line_y = self.y + i * self.line_spacing
            text_rect = text_surface.get_rect(center=(self.x, line_y))
            screen.blit(text_surface, text_rect)
