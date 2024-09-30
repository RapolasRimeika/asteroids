import pygame                                      # Pygame library for rendering and surface manipulation
import random                                      # Random library for generating random positions and sizes
from PIL import Image, ImageFilter                 # PIL for applying Gaussian blur to planet textures

def generate_star_and_planet_background(screen_width, screen_height, num_stars, num_planets, color_range):
    """Generates a space-themed background with stars and planets, including Gaussian blur on planets."""
    stars_surface = generate_stars(screen_width, screen_height, num_stars, color_range)                # Step 1: Generate stars
    planets_surface = generate_planets(screen_width, screen_height, num_planets, color_range)          # Step 2: Generate planets
    blurred_planets_surface = apply_blur_to_planets(planets_surface)                                   # Step 3: Apply Gaussian blur
    final_background = combine_stars_and_planets(stars_surface, blurred_planets_surface)               # Step 4: Combine stars and planets
    return final_background

def generate_stars(screen_width, screen_height, num_stars, color_range):
    """Generates a surface with random stars."""
    stars_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)  # Create a transparent surface
    stars_surface.fill((8, 8, 20))                                                  # Dark background for space
    for _ in range(num_stars):
        x = random.randint(0, screen_width)                                         # Random X position for star
        y = random.randint(0, screen_height)                                        # Random Y position for star
        star_size = random.randint(1, 2)                                            # Random star size (1-2 pixels)
        star_color = (random.randint(*color_range),                                 # Random star color
                      random.randint(*color_range), 
                      random.randint(*color_range))
        pygame.draw.circle(stars_surface, star_color, (x, y), star_size)            # Draw the star as a small circle
    return stars_surface

def generate_planets(screen_width, screen_height, num_planets, color_range):
    """Generates a surface with random planets."""
    planets_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)  # Create transparent surface for planets
    for _ in range(num_planets):
        x = random.randint(0, screen_width)                                           # Random X position for planet
        y = random.randint(0, screen_height)                                          # Random Y position for planet
        planet_radius = random.randint(30, 100)                                       # Random radius for planet
        planet_color = (random.randint(*color_range),                                 # Random planet color
                        random.randint(*color_range), 
                        random.randint(*color_range))
        pygame.draw.circle(planets_surface, planet_color, (x, y), planet_radius)      # Draw planet as a large circle
        for _ in range(random.randint(20, 50)):                                       # Add random noise/texture
            noise_x = x + random.randint(-planet_radius, planet_radius)               # Random noise position near planet
            noise_y = y + random.randint(-planet_radius, planet_radius)
            noise_size = random.randint(1, 5)                                         # Random noise size
            noise_color = (random.randint(50, 100), random.randint(50, 150), random.randint(50, 100))  # Noise color
            pygame.draw.circle(planets_surface, noise_color, (noise_x, noise_y), noise_size)           # Draw noise
    return planets_surface

def apply_blur_to_planets(planets_surface):
    """Applies Gaussian blur to the planet surface using Pillow."""
    str_format = pygame.image.tostring(planets_surface, "RGBA")                       # Convert Pygame surface to Pillow image
    img = Image.frombytes("RGBA", planets_surface.get_size(), str_format)             # Create Pillow image
    img = img.filter(ImageFilter.GaussianBlur(radius=2))                              # Apply Gaussian blur with radius 2
    blurred_str = img.tobytes()                                                       # Convert back to Pygame surface
    blurred_planets_surface = pygame.image.fromstring(blurred_str, planets_surface.get_size(), "RGBA")
    return blurred_planets_surface

def combine_stars_and_planets(stars_surface, planets_surface):
    """Combines the star and planet surfaces into a final background."""
    final_surface = stars_surface.copy()                                              # Copy star surface as base
    final_surface.blit(planets_surface, (0, 0))                                       # Overlay planets onto the stars
    return final_surface