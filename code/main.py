import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from tile import Tile


class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.tile_size = 64
        pygame.display.set_caption('Contra shooter')
        
        # groups
        self.all_sprites = pygame.sprite.Group()
        
        self.setup()
    
    def setup(self):
        tmx_map = load_pygame('data/map.tmx')
        
        for x, y, surf in tmx_map.get_layer_by_name('Level').tiles():
            Tile(pos=(x * self.tile_size, y * self.tile_size), surf=surf, groups=self.all_sprites)
    
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
            self.all_sprites.draw(surface=self.screen)
            
            pygame.display.update()
        
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run(is_run=True)
