import pygame
from pygame.math import Vector2
from player import Player
from pytmx.util_pygame import load_pygame


class CameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = Vector2()
        
        # imports
        self.bg_sky = pygame.image.load(file='graphics/sky/bg_sky.png').convert_alpha()
        self.fg_sky = pygame.image.load(file='graphics/sky/fg_sky.png').convert_alpha()
        map_tmx = load_pygame(filename='data/map.tmx')
        
        # dimensions
        self.padding = self.screen.get_width() / 2
        self.sky_width = self.bg_sky.get_width()
        self.map_width = map_tmx.width * map_tmx.tilewidth + (2 * self.padding)
        self.sky_count = int(self.map_width // self.sky_width)
    
    def draw_custom(self, player):
        if not isinstance(player, Player):
            raise(f'{player} object is not Player class.')

        self.offset.x = player.rect.centerx - (self.screen.get_width() / 2)
        self.offset.y = player.rect.centery - (self.screen.get_height() / 2)
        
        for sky_index in range(self.sky_count):
            x_pos = -self.padding + (sky_index * self.sky_width)
            self.screen.blit(source=self.bg_sky, dest=(x_pos - self.offset.x / 2.5, 800 - self.offset.y / 2.5))
            self.screen.blit(source=self.fg_sky, dest=(x_pos - self.offset.x / 2, 800 - self.offset.y / 2))
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.screen.blit(source=sprite.image, dest=offset_rect)
    