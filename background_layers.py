import pygame
import random
from PIL import Image, ImageFilter
from constants import *

class Background:
    def __init__(self, screen_width, screen_height):
        # Initialize the background layers
        self.layers = [
            self.generate_star_layer(screen_width, screen_height, 10000, (5, 80)),  # Star layer (middle)
            self.generate_star_layer(screen_width, screen_height, 500, (50, 110)),  # Star layer (middle)
            self.generate_planet_layer(screen_width, screen_height, 3, (50, 100))   # Planet layer (closest)
        ]
        self.parallax_factors = [0.01, 0.03, 0.1]
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

    def generate_star_layer(self, width, height, num_stars, color_range):
        layer = pygame.Surface((width, height), pygame.SRCALPHA)
        for _ in range(num_stars):
            x = random.randint(0, width)
            y = random.randint(0, height)
            star_size = random.randint(1, 2)
            star_color = (random.randint(*color_range), random.randint(*color_range), random.randint(*color_range))
            pygame.draw.circle(layer, star_color, (x, y), star_size)
        return layer

    def generate_planet_layer(self, width, height, num_planets, color_range, blur_radius=1):
        # Create the surface for planets
        layer = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Draw the planets
        for _ in range(num_planets):
            x = random.randint(0, width)
            y = random.randint(0, height)
            planet_radius = random.randint(30, 100)
            planet_color = (random.randint(*color_range), random.randint(*color_range), random.randint(*color_range))
            pygame.draw.circle(layer, planet_color, (x, y), planet_radius)

        # Convert Pygame surface to a Pillow Image
        str_format = pygame.image.tostring(layer, "RGBA")
        img = Image.frombytes("RGBA", (width, height), str_format)

        # Apply Gaussian blur using Pillow
        img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        # Convert the Pillow Image back to Pygame surface
        blurred_str = img.tobytes()
        layer = pygame.image.fromstring(blurred_str, (width, height), "RGBA")

        return layer

    def update(self, dt, player_position):
        # Update parallax offsets based on player position and parallax factor
        self.offsets = [
            (-player_position.x * self.parallax_factors[i] % self.screen_width, 
             -player_position.y * self.parallax_factors[i] % self.screen_height)
            for i in range(len(self.layers))
        ]

    def draw(self, screen):
        for layer in self.layers:
            screen.blit(layer, (0, 0))  # Draw layers without offsets for now


""" def draw(self, screen):
        for i, layer in enumerate(self.layers):
            layer_offset_x, layer_offset_y = self.offsets[i]

            # Draw the primary layer
            screen.blit(layer, (layer_offset_x, layer_offset_y))

            # Handle horizontal and vertical wrapping
            if layer_offset_x < 0:  # Draw an additional tile to the right
                screen.blit(layer, (layer_offset_x + self.screen_width, layer_offset_y))
            if layer_offset_y < 0:  # Draw an additional tile below
                screen.blit(layer, (layer_offset_x, layer_offset_y + self.screen_height))

            # Handle the corner case: draw extra layer if both x and y offsets are less than 0
            if layer_offset_x < 0 and layer_offset_y < 0:
                screen.blit(layer, (layer_offset_x + self.screen_width, layer_offset_y + self.screen_height))

"""

def generate_star_background(screen_width, screen_height, num_stars, color_range):
    # Create a surface for the background with a black color
    background = pygame.Surface((screen_width, screen_height))
    background.fill((0, 0, 0))  # Fill the background with black

    # Draw stars on the background
    for _ in range(num_stars):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        star_size = random.randint(1, 2)
        star_color = (random.randint(*color_range), random.randint(*color_range), random.randint(*color_range))
        pygame.draw.circle(background, star_color, (x, y), star_size)

    return background