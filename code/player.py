import os

import pygame
from pygame.math import Vector2
from settings import *


class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, path, collision_sprites):
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
        
        # collisions
        self.old_rect = self.rect.copy()
        self.collision_sprites = collision_sprites
        
        # vertical movement
        self.gravity = 15
        self.jump_speed = 1900
        self.on_floor = False
        self.duck = True
    
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
    
    def get_status(self):
        # idle
        if self.direction.x == 0 and self.on_floor:
            self.status = self.status.split('_')[0] + '_idle'
        
        # jump
        if self.direction.y != 0 and not self.on_floor:
            self.status = self.status.split('_')[0] + '_jump'
        
        # Duck
        if self.duck and self.on_floor:
            self.status = self.status.split('_')[0] + '_duck'
    
    def check_contact(self):
        bottom_rect = pygame.Rect(0, 0, self.rect.width, 5)
        bottom_rect.midtop = self.rect.midbottom
        
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True
    
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    # left collision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    
                    self.pos.x = self.rect.x
                if direction == 'vertical':
                    # top collsion
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    
                    # bottom collision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.on_floor = True
                    
                    self.pos.y = self.rect.y
                    self.direction.y = 0
        
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False
    
    def move(self, dt):
        if self.duck and self.on_floor:
            self.direction.x = 0
        
        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision(direction='horizontal')
        
        # vertical
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt
        self.rect.y = round(self.pos.y)
        self.collision(direction='vertical')
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        # horizontal
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0
        
        if keys[pygame.K_w] and self.on_floor:
            self.direction.y = -self.jump_speed
        
        if keys[pygame.K_s]:
            self.duck = True
        else:
            self.duck = False
    
    def animate(self, dt):
        self.frame_count += 7 * dt
        if self.frame_count >= len(self.animations[self.status]):
            self.frame_count = 0
        
        self.image = self.animations[self.status][int(self.frame_count)]
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.get_status()
        self.move(dt)
        self.check_contact()
        self.animate(dt)
