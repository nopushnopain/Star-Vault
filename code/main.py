import sys

import pygame
from debug import debug  # auxilia implementacao das parada (nao importante)
from mapa import Mapa
from settings import *


class Game:
    def __init__(self):
        
        # setup geral
        pygame.init()
        pygame.display.set_caption("Star Vault")
        self.screen = pygame.display.set_mode((LARGURA, ALTURA)) # importado do settings
        self.clock = pygame.time.Clock()
        self.mapa = Mapa() # inicializa o mapa
        
    def run(self):
        while True:
            
            # fecha no x
            for acao in pygame.event.get(): 
                if acao.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen.fill('black')
            self.mapa.run()
            pygame.display.update()
            self.clock.tick(FPS) # fps do jogo importado do settings
        
if __name__ == '__main__':
    game = Game()
    game.run()