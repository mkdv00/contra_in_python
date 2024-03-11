import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, LAYERS


class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Contra shooter')
    
    def run(self, is_run: bool = True):
        while is_run:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_run = False
                
            # delta time
            dt = self.clock.tick() / 1000
            
            # bg
            self.screen.fill((249, 131, 103))
            
            pygame.display.update()
        
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run(is_run=True)
