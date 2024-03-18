import pygame
from entity import Entity
from pygame.math import Vector2
from settings import *


class Enemy(Entity):
    
    def __init__(self, pos, groups, path, shoot, player, collision_sprites):
        super().__init__(pos, groups, path, shoot)
        
        self.player = player
        for sprite in collision_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top
        
        self.shoot_colldown = 900
        self.duck = False
        self.invulerable_cooldown = 200
    
    def get_status(self):
        if self.player.rect.centerx < self.rect.centerx:
            self.status = 'left'
        else:
            self.status = 'right'
    
    def check_fire(self):
        player_pos = Vector2(self.player.rect.center)
        enemy_pos = Vector2(self.rect.center)
        
        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False
        
        if distance < 600 and same_y and self.can_shoot:
            bullet_direction = Vector2(1, 0) if self.status == 'right' else Vector2(-1, 0)
            y_offset = Vector2(0, -16)
            pos = self.rect.center + bullet_direction * 80
            self.shoot(pos + y_offset, bullet_direction, self)
            
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def update(self, dt):
        self.get_status()
        self.animate(dt)
        self.blink()
        self.invulerable_timer()
        
        self.shoot_timer()
        self.check_fire()
        
        # Check death
        self.check_death()
        