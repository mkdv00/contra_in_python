import pygame
from player import Player


class Overlay:
    
    def __init__(self, player):
        self.screen = pygame.display.get_surface()
        self.player = player
        self.health_surf = pygame.image.load('graphics/health.png').convert_alpha()
    
    def display(self):
        for i in range(self.player.health):
            x_pos = 10 + i * (self.health_surf.get_width() + 3)
            self.screen.blit(source=self.health_surf, dest=(x_pos, 10))
    