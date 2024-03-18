import sys

import pygame
from entity import Entity
from pygame.math import Vector2
from settings import *


class Player(Entity):
    
    def __init__(self, pos, groups, path, collision_sprites, shoot):
        super().__init__(pos, groups, path, shoot)
        
        # collisions
        self.collision_sprites = collision_sprites
        
        # vertical movement
        self.gravity = 15
        self.jump_speed = 1900
        self.on_floor = False
        self.moving_platform = None
        
        self.health = 10
    
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
    
    def check_death(self):
        if self.health <= 0:
            pygame.quit()
            sys.exit() 
    
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
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.shoot_timer()
        self.invulerable_timer()
        self.get_status()
        self.move(dt)
        self.check_contact()
        self.animate(dt)
        self.blink()
        
        # Check death
        self.check_death()
