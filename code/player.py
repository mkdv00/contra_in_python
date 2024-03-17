import os

import pygame
from pygame.math import Vector2
from settings import *


class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, path, collision_sprites, shoot):
        super().__init__(groups)
        
        # setup the player
        self.import_assets(path=path)
        self.frame_count = 0
        self.status = 'right'
        
        self.image = self.animations[self.status][self.frame_count]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['Level']
    
        # movement
        self.velocity = Vector2()
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
        self.moving_platform = None
        
        # interaction
        self.shoot = shoot
        
        # shoot timer
        self.shoot_time = None
        self.can_shoot = True
        self.shoot_colldown = 200
    
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
                if hasattr(sprite, 'direction'):
                    self.moving_platform = sprite
    
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
        
        if self.direction.x == 0:
            self.velocity = Vector2()
        
        # horizontal
        self.velocity.x = self.direction.x * self.speed
        self.pos.x += self.velocity.x * dt
        self.rect.x = round(self.pos.x)
        self.collision(direction='horizontal')
        
        # vertical
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt
        
        # check on the platform
        if self.moving_platform and self.moving_platform.direction.y > 0 and self.direction.y > 0:
            self.direction.y = 0
            self.rect.bottom = self.moving_platform.rect.top
            self.pos.y = self.rect.y
            self.on_floor = True
        
        self.rect.y = round(self.pos.y)
        self.collision(direction='vertical')
        self.moving_platform = None
    
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
        
        # interactions
        if keys[pygame.K_SPACE] and self.can_shoot:
            direction = Vector2(1, 0) if self.status.split('_')[0] == 'right' else Vector2(-1, 0)
            pos = self.rect.center + direction * 60
            y_offset = Vector2(0, -16) if not self.duck else Vector2(0, 10)
            self.shoot(pos + y_offset, direction, self)
            
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.shoot_time > self.shoot_colldown:
                self.can_shoot = True
    
    def animate(self, dt):
        self.frame_count += 7 * dt
        if self.frame_count >= len(self.animations[self.status]):
            self.frame_count = 0
        
        self.image = self.animations[self.status][int(self.frame_count)]
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.shoot_timer()
        self.get_status()
        self.move(dt)
        self.check_contact()
        self.animate(dt)
