import pygame
from constants import *
from player import Player

class State():
    def __init__(self, player_dead):
        self.player_dead = player_dead
        self.player = None

    def update(self, dt, updatable, drawable):
        keys = pygame.key.get_pressed()
        if  self.player_dead and keys[pygame.K_RETURN]:
            print("enter pressed and player dead")
            self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            updatable.add(self.player)
            drawable.add(self.player)
            self.player_dead = False