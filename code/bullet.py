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


class FireAnimations(pygame.sprite.Sprite):
    
    def __init__(self, entity, surf_list, direction, groups):
        super().__init__(groups)
        
        # setup
        self.entity = entity
        self.frames = surf_list
        if direction.x < 0:
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]
        
        # offset
        offset_x = -60 if direction.x < 0 else 60
        offset_y = 10 if entity.duck else -16
        self.offset = Vector2(offset_x, offset_y)
        
        # image
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=self.entity.rect.center + self.offset)
        self.z = LAYERS['Level']
    
    def animate(self, dt):
        self.frame_index += 15 * dt
        
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    
    def move(self):
        self.rect.center = self.entity.rect.center + self.offset
    
    def update(self, dt):
        self.animate(dt)
        self.move()
