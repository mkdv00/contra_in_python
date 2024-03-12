import pygame
from pygame.math import Vector2

from settings import *


class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size=(40, 80))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['Level']
    
        # movement
        self.pos = Vector2(self.rect.topleft)
        self.direction = Vector2()
        self.speed = 400
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        # horizontal
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        # vertical
        if keys[pygame.K_s]:
            self.direction.y = 1
        elif keys[pygame.K_w]:
            self.direction.y = -1
        else:
            self.direction.y = 0
    
    def move(self, dt):
        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        
        # vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
    
    def update(self, dt):
        self.input()
        self.move(dt)
