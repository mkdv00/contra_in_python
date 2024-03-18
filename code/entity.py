import os
from math import sin

import pygame
from pygame.math import Vector2
from settings import *


class Entity(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, path, shoot):
        super().__init__(groups)
        
        # graphics setup
        self.import_assets(path=path)
        self.frame_count = 0
        self.status = 'right'
        
        # image
        self.image = self.animations[self.status][self.frame_count]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = LAYERS['Level']
        self.mask = pygame.mask.from_surface(self.image)
        
        # float based movement
        self.velocity = Vector2()
        self.pos = Vector2(self.rect.topleft)
        self.direction = Vector2()
        self.speed = 400
        
        # shoot
        self.shoot = shoot
        self.shoot_time = None
        self.can_shoot = True
        self.shoot_colldown = 200
        self.duck = True
        
        # health
        self.health = 3
        self.can_take_damage = True
        self.invulerable_time = None
        self.invulerable_cooldown = 500
    
    def blink(self):
        if not self.can_take_damage:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0, 0, 0))
                self.image = white_surf

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return True
        else: return False
    
    def damage(self, damage_amount):
        if self.can_take_damage:
            self.health -= damage_amount
            
            self.invulerable_time = pygame.time.get_ticks()
            self.can_take_damage = False
    
    def invulerable_timer(self):
        if not self.can_take_damage:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.invulerable_time > self.invulerable_cooldown:
                self.can_take_damage = True
    
    def check_death(self):
        if self.health <= 0:
            self.kill()
    
    def animate(self, dt):
        self.frame_count += 7 * dt
        if self.frame_count >= len(self.animations[self.status]):
            self.frame_count = 0
        
        self.image = self.animations[self.status][int(self.frame_count)]
        self.mask = pygame.mask.from_surface(self.image)
    
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
    
    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.shoot_time > self.shoot_colldown:
                self.can_shoot = True
