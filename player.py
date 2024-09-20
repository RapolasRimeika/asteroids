from constants import *
from circleshape import CircleShape
import pygame

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0 #initialize rotation attribute
        
#defining the triangle shape that rotates    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5 # type: ignore
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

# Draws a triangle shape on the screen using pygame's draw.polygon method
# - screen: The surface to draw the triangle on (passed in as an argument)
# - "white": The color of the triangle's outline
# - self.triangle(): A list of points representing the vertices of the triangle
# - 2: The width of the triangle's outline (if 0, it would fill the shape)
    def draw(self, screen):
        points = self.triangle()
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)
        print(f"drawing white triangle with points: {points}")
