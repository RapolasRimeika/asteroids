"""
Class for displaying floating text messages on the screen for a limited duration.

FloatingText objects are automatically added to sprite groups and handle rendering multi-line
messages with customizable font size, color, and spacing. The text appears at a specified 
(x, y) position and disappears after a given duration.
"""

import pygame
from constants import *

class FloatingText(pygame.sprite.Sprite):
    containers = []  # Set to relevant sprite groups in the main loop

    def __init__(self, x, y, message, RGB, duration, line_spacing=LINE_SPACING):
        super().__init__(self.containers)                     # Automatically add to all specified sprite groups
        self.x = x                                            # X-coordinate of text
        self.y = y                                            # Y-coordinate of text
        self.message = message                                # The message to display
        self.duration = duration                              # Duration for the text to stay visible
        self.RGB = RGB                                        # Text color in RGB format
        self.start_time = pygame.time.get_ticks()             # Start time for tracking the duration
        self.font = pygame.font.Font(None, FONT_SIZE)         # Font size for rendering the text
        self.line_spacing = line_spacing                      # Line spacing for multi-line messages
        self.render_lines()                                   # Pre-render the text surfaces

    def render_lines(self):
        """Splits the message into multiple lines and creates a surface for each."""
        self.lines = self.message.split('\n')                 # Split message by line breaks
        self.text_surfaces = []                               # List to store rendered text surfaces
        for line in self.lines:
            text_surface = self.font.render(line, True, self.RGB)  # Render each line of text
            self.text_surfaces.append(text_surface)           # Add the rendered line to the list

    def update(self, dt):
        current_time = pygame.time.get_ticks()                # Get current time
        if current_time - self.start_time > self.duration:    # Check if the text's duration has expired
            self.kill()                                       # Remove the floating text after its duration

    def draw(self, screen):
        """Draw each line of text with appropriate line spacing."""
        for i, text_surface in enumerate(self.text_surfaces):     # Loop through each text surface (line)
            line_y = self.y + i * self.line_spacing               # Calculate Y position for each line
            text_rect = text_surface.get_rect(center=(self.x, line_y))  # Center the text at (x, line_y)
            screen.blit(text_surface, text_rect)                  # Draw the text on the screen
