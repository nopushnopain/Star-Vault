import pygame
from debug import debug
from ladrilho import Ladrilho
from player import Player
from settings import * # * significa tudo


class Mapa:
    def __init__(self):
        
        # exibe a superficie
        self.display_superficie = pygame.display.get_surface()
        
        # seta o grupo do sprite
        self.sprites_visiveis = classificaCameraY()
        self.sprites_obstaculos = pygame.sprite.Group()
        
        # seta o sprite
        self.criar_mapa()
        
    def criar_mapa(self):
        # for idx_linha, linha in enumerate(WORLD_MAP):
        #     for idx_coluna, coluna in enumerate(linha):
        #         x = idx_coluna * LADRILHOSIZE
        #         y = idx_linha  * LADRILHOSIZE
        #         if coluna == 'x':
        #             Ladrilho((x,y), [self.sprites_visiveis, self.sprites_obstaculos])
        #         if coluna == 'p':
        #             self.player = Player((x,y), [self.sprites_visiveis], self.sprites_obstaculos)
        self.player = Player((2000,1430), [self.sprites_visiveis], self.sprites_obstaculos)                        
    def run(self):
        # atualiza e desenha o jogo
        self.sprites_visiveis.customizaDesenho(self.player)
        self.sprites_visiveis.update()
    
class classificaCameraY(pygame.sprite.Group):
    def __init__(self):
        
        # setup geral
        super().__init__()
        self.display_superficie = pygame.display.get_surface()
        self.metade_largura = self.display_superficie.get_size()[0] // 2 # pega metade da figura
        self.metade_altura = self.display_superficie.get_size()[1] // 2
        self.deslocamento = pygame.math.Vector2(100, 200) # deslocamento da camera
        
        # criando o chao
        self.superficieDoChao = pygame.image.load('graficos/tilemap/ground.png').convert()
        self.superficieDoRetangulo = self.superficieDoChao.get_rect(topleft = (0,0))

    def customizaDesenho(self, player):
        
        # pega o deslocamento
        self.deslocamento.x = player.rect.centerx - self.metade_largura
        self.deslocamento.y = player.rect.centery - self.metade_altura
        
        # desenhando o chao
        deslocamento_chao_posicao = self.superficieDoRetangulo.topleft - self.deslocamento
        self.display_superficie.blit(self.superficieDoChao, deslocamento_chao_posicao)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            posicao_deslocado = sprite.rect.topleft - self.deslocamento
            self.display_superficie.blit(sprite.image, posicao_deslocado)