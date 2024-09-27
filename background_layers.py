import pygame
import random
from PIL import Image, ImageFilter 


def generate_star_and_planet_background(screen_width, screen_height, num_stars, num_planets, color_range):
    # Step 1: Generate stars
    stars_surface = generate_stars(screen_width, screen_height, num_stars, color_range)
    # Step 2: Generate planets with random textures
    planets_surface = generate_planets(screen_width, screen_height, num_planets, color_range)
    # Step 3: Apply Gaussian blur to the planets
    blurred_planets_surface = apply_blur_to_planets(planets_surface)
    # Step 4: Combine stars and blurred planets
    final_background = combine_stars_and_planets(stars_surface, blurred_planets_surface)
    return final_background

def generate_stars(screen_width, screen_height, num_stars, color_range):
    # Create a surface for the stars
    stars_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    stars_surface.fill((5, 5, 15))  # Fill with black or dark color for space

    # Draw random stars
    for _ in range(num_stars):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        star_size = random.randint(1, 2)
        star_color = (random.randint(*color_range), random.randint(*color_range), random.randint(*color_range))
        pygame.draw.circle(stars_surface, star_color, (x, y), star_size)
    return stars_surface

def generate_planets(screen_width, screen_height, num_planets, color_range):
    # Create a surface for the planets
    planets_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    # Draw random planets as circles with random textures
    for _ in range(num_planets):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        planet_radius = random.randint(30, 100)
        planet_color = (random.randint(*color_range), random.randint(*color_range), random.randint(*color_range))
        pygame.draw.circle(planets_surface, planet_color, (x, y), planet_radius)
        # Add random noise or texture to the planets (e.g., by drawing random smaller circles)
        for _ in range(random.randint(20, 50)):
            noise_x = x + random.randint(-planet_radius, planet_radius)
            noise_y = y + random.randint(-planet_radius, planet_radius)
            noise_size = random.randint(1, 5)
            noise_color = (random.randint(50, 100), random.randint(50, 150), random.randint(50, 100))
            pygame.draw.circle(planets_surface, noise_color, (noise_x, noise_y), noise_size)
    return planets_surface

def apply_blur_to_planets(planets_surface):
    # Convert Pygame surface to Pillow Image for Gaussian blur
    str_format = pygame.image.tostring(planets_surface, "RGBA")
    img = Image.frombytes("RGBA", planets_surface.get_size(), str_format)
    # Apply Gaussian blur to the planets
    img = img.filter(ImageFilter.GaussianBlur(radius=2))  # Adjust blur radius as needed
    # Convert back to Pygame surface
    blurred_str = img.tobytes()
    blurred_planets_surface = pygame.image.fromstring(blurred_str, planets_surface.get_size(), "RGBA")
    return blurred_planets_surface

def combine_stars_and_planets(stars_surface, planets_surface):
    # Create a final surface to combine the stars and blurred planets
    final_surface = stars_surface.copy()
    # Blit the blurred planets onto the starry background
    final_surface.blit(planets_surface, (0, 0))

    return final_surface



