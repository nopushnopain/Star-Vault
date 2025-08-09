import pygame
from debug import debug  # noqa: F401
from ladrilho import Ladrilho  # noqa: F401
from player import Player
from settings import * # * significa tudo  # noqa: F403
from suporte import *  # noqa: F403
from random import choice


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
        layouts = {
            'limite': import_csv_layout('mapa/mapa_blocoschao.csv'),  # noqa: F405
            'grama': import_csv_layout('mapa/mapa_grama.csv'),  # noqa: F405
            'objetos': import_csv_layout('mapa/mapa_objetos.csv')  # noqa: F405
        }
        graficos = {
            'grama': importa_pasta('graficos/grama'),  # noqa: F405
            'objetos': importa_pasta('graficos/objetos')  # noqa: F405
        }
        for estilo, layout in layouts.items():
            for idx_linha, linha in enumerate(layout):
                for idx_coluna, coluna in enumerate(linha):
                    if coluna != '-1':
                        x = idx_coluna * LADRILHOSIZE  # noqa: F405
                        y = idx_linha  * LADRILHOSIZE  # noqa: F405
                        if estilo == 'limite':
                            Ladrilho((x,y), [self.sprites_obstaculos], 'invisivel')
                        # cria o ladrilho da grama
                        if estilo == 'grass':
                            imagem_grama_random = choice(graficos['grama'])
                            Ladrilho((x,y),[self.sprites_visiveis, self.sprites_obstaculos], 'grama', imagem_grama_random)
                        if estilo == 'objetos':
                            superficie = graficos['objetos'][int(coluna)]
                            Ladrilho((x,y), [self.sprites_visiveis, self.sprites_obstaculos],'objetos', superficie)
        

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