class Player(CircleShape):
    def__init__(self, x, y)
    super().__init__(PLAYER_RADIUS)
    
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
    self.pygame.draw.polygon(screen, "white", self.triangle(), 2)
