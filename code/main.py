import pygame
from player import Player
from pytmx.util_pygame import load_pygame
from settings import *
from tile import Tile, CollisionTile
from camera import CameraGroup


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
        
        self.setup()
    
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
                self.player = Player(pos=(obj.x, obj.y), groups=self.all_sprites, 
                                     path='graphics/player', collision_sprites=self.collision_sprites)
    
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
            self.all_sprites.update(dt)
            
            # draw
            self.all_sprites.draw_custom(player=self.player)
            
            pygame.display.update()
        
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run(is_run=True)
