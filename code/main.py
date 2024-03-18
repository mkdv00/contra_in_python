import pygame
from bullet import Bullet, FireAnimations
from camera import CameraGroup
from enemy import Enemy
from overlay import Overlay
from player import Player
from pytmx.util_pygame import load_pygame
from settings import *
from tile import CollisionTile, MovingPlatform, Tile


class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.tile_size = 64
        pygame.display.set_caption('Contra shooter')
        
        # groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.vulnerable_sprites = pygame.sprite.Group()
        
        self.setup()
        self.overlay = Overlay(player=self.player)
        
        # bullets sprites
        self.bullet_surf = pygame.image.load('graphics/bullet.png').convert_alpha()
        self.fire_surfs = [
            pygame.image.load('graphics/fire/0.png').convert_alpha(),
            pygame.image.load('graphics/fire/1.png').convert_alpha()
        ]
        
        # music
        self.bullet_sound = pygame.mixer.Sound(file='audio/bullet.wav')
        self.bullet_sound.set_volume(0.15)
        
        self.hit_sound = pygame.mixer.Sound(file='audio/hit.wav')
        self.hit_sound.set_volume(0.15)
        
        self.music = pygame.mixer.Sound(file='audio/music.wav')
        self.music.set_volume(0.3)
        self.music.play(loops=-1)
    
    def setup(self):
        tmx_map = load_pygame('data/map.tmx')
        layers = ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']
        
        # Collision Tiles
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            CollisionTile(pos=(x * self.tile_size, y * self.tile_size), surf=surf, 
                          groups=[self.all_sprites, self.collision_sprites])
        
        # Tiles
        for layer in layers:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile(pos=(x * self.tile_size, y * self.tile_size), 
                     surf=surf, groups=self.all_sprites, z=LAYERS[layer])
        
        # Objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(pos=(obj.x, obj.y),
                                     groups=[self.all_sprites, self.vulnerable_sprites],
                                     path='graphics/player', 
                                     collision_sprites=self.collision_sprites,
                                     shoot=self.shoot)
            if obj.name == 'Enemy':
                Enemy(pos=(obj.x, obj.y),
                      groups=[self.all_sprites, self.vulnerable_sprites], 
                      path='graphics/enemies/standard', 
                      shoot=self.shoot, 
                      player=self.player,
                      collision_sprites=self.collision_sprites)
        
        # Platforms
        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name('Platforms'):
            if obj.name == 'Platform':
                MovingPlatform(pos=(obj.x, obj.y), surf=obj.image,
                               groups=[self.all_sprites, self.collision_sprites, self.platform_sprites])
            else:
                platform_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border_rects.append(platform_rect)
    
    def platform_collisions(self):
        for platform in self.platform_sprites.sprites():
            for border in self.platform_border_rects:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0:
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else:
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1
            
            if platform.rect.colliderect(self.player.rect) and self.player.rect.centery > platform.rect.centery:
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1
    
    def bullet_collisions(self):
        # obstacles
        for obstacle in self.collision_sprites.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullet_sprites, True)
        
        # entities
        for sprite in self.vulnerable_sprites.sprites():
            if pygame.sprite.spritecollide(sprite, self.bullet_sprites, True, pygame.sprite.collide_mask):
                sprite.damage(damage_amount=1)
                self.hit_sound.play(loops=1)
    
    def shoot(self, pos, direction, entity):
        FireAnimations(entity=entity, surf_list=self.fire_surfs, direction=direction, groups=self.all_sprites)
        Bullet(pos, self.bullet_surf, direction, [self.all_sprites, self.bullet_sprites])
        self.bullet_sound.play(loops=1)
    
    def run(self, is_run: bool = True):
        while is_run:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_run = False
                
            # delta time
            dt = self.clock.tick() / 1000
            
            # bg
            self.screen.fill((249, 131, 103))
            
            # updates
            self.platform_collisions()
            self.all_sprites.update(dt)
            self.bullet_collisions()
            
            # draw
            self.all_sprites.draw_custom(player=self.player)
            self.overlay.display()
            
            pygame.display.update()
        
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run(is_run=True)
