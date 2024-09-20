import pygame
print("Starting asteroids!")

from constants import *

print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

color = (0, 0, 0)
running = True
while running:
    screen.fill((0, 0, 0))
    pygame.display.flip()

#this will check if player closed the window and stop the game loop if they do.
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        return
