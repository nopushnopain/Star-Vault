import pygame
from settings import *
from ladrilho import Ladrilho
from player import Player
from debug import debug


class Mapa:
    def __init__(self):
        
        # exibe a superficie
        self.display_superficie = pygame.display.get_surface()
        
        # seta o grupo do sprite
        self.sprites_visiveis = pygame.sprite.Group()
        self.sprites_obstaculos = pygame.sprite.Group()
        
        # seta o sprite
        self.criar_mapa()
        
        
    def criar_mapa(self):
        for idx_linha, linha in enumerate(WORLD_MAP):
            for idx_coluna, coluna in enumerate(linha):
                x = idx_coluna * LADRILHOSIZE
                y = idx_linha  * LADRILHOSIZE
                if coluna == 'x':
                    Ladrilho((x,y), [self.sprites_visiveis, self.sprites_obstaculos])
                if coluna == 'p':
                    self.player = Player((x,y), [self.sprites_visiveis], self.sprites_obstaculos)
                    
    
    
    
    
    def run(self):
        # atualiza e desenha o jogo
        self.sprites_visiveis.draw(self.display_superficie)
        self.sprites_visiveis.update()
        debug(self.player.direction)
        
        