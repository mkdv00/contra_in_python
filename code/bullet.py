import pygame
from pygame.math import Vector2
from settings import *


class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, pos, surf, direction, groups):
        super().__init__(groups)
        self.image = surf if direction.x > 0 else pygame.transform.flip(surf, flip_x=True, flip_y=False)
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['Level']
        
        # float based movement
        self.direction = direction
        self.pos = Vector2(self.rect.center)
        self.speed = 1200
        
        # bullet timer
        self.start_time = pygame.time.get_ticks()
        self.visible_colldown = 1000
    
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
        if pygame.time.get_ticks() - self.start_time > self.visible_colldown:
            self.kill()
