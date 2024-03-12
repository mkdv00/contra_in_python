import pygame
from pygame.math import Vector2
from player import Player


class CameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = Vector2()
    
    def draw_custom(self, player):
        if not isinstance(player, Player):
            raise(f'{player} object is not Player class.')

        self.offset.x = player.rect.centerx - (self.screen.get_width() / 2)
        self.offset.y = player.rect.centery - (self.screen.get_height() / 2)
        
        for sprite in self.sprites():
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.screen.blit(source=sprite.image, dest=offset_rect)
    