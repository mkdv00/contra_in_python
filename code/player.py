import os

import pygame
from pygame.math import Vector2
from settings import *


class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, path):
        super().__init__(groups)
        
        # setup the player
        self.import_assets(path=path)
        self.frame_count = 0
        self.status = 'right'
        
        self.image = self.animations[self.status][self.frame_count]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['Level']
    
        # movement
        self.pos = Vector2(self.rect.topleft)
        self.direction = Vector2()
        self.speed = 400
    
    def import_assets(self, path):
        self.animations = {}
        
        for index, folder in enumerate(os.walk(path)):
            if index == 0:
                for key in folder[1]:
                    self.animations[key] = []
            else:
                for file in sorted(folder[2], key=lambda file_name: int(file_name.split('.')[0])):
                    file_path = folder[0].replace('\\', '/') + '/' + file
                    key = file_path.split('/')[-2]
                    self.animations[key].append(pygame.image.load(file=file_path).convert_alpha())
    
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
    
    def animate(self, dt):
        self.frame_count += 7 * dt
        if self.frame_count >= len(self.animations[self.status]):
            self.frame_count = 0
        
        self.image = self.animations[self.status][int(self.frame_count)]
    
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
