import pygame
from debug import debug  # depuração
from ladrilho import Ladrilho
from player import Jogador
from settings import * 
from suporte import *  
from random import choice
from inimigo import enemy

class Mapa:
    def __init__(self):
        # referência à superfície da janela
        self.superficie_display = pygame.display.get_surface()
        
        # grupos de sprites
        self.sprites_visiveis = GrupoCamera()
        self.sprites_colisao = pygame.sprite.Group()
        
        # cria o mapa
        self.criar_mapa()
        
    def criar_mapa(self):
        # layouts de mapa via CSV
        layouts = {
            'limite': import_csv_layout('mapa_csv/mapa_blocoschao.csv'),
            'grama': import_csv_layout('mapa_csv/mapa_grama.csv'),
            'objetos': import_csv_layout('mapa_csv/mapa_objetos.csv'),
            'inimigos': import_csv_layout('mapa_csv/mapa_inimigos.csv')
        }
        # imagens do mapa
        graficos = {
            'grama': importa_pasta('graficos/grama'),
            'objetos': importa_pasta('graficos/objetos'),

        }
        # geração de elementos do mapa
        for tipo, layout in layouts.items():
            for linha_idx, linha in enumerate(layout):
                for coluna_idx, valor in enumerate(linha):
                    if valor != '-1':
                        x = coluna_idx * LADRILHOSIZE
                        y = linha_idx  * LADRILHOSIZE
                        if tipo == 'limite':
                            Ladrilho((x, y), [self.sprites_colisao], 'invisivel')
                        elif tipo == 'grama':
                            grama_random = choice(graficos['grama'])
                            Ladrilho((x, y), [self.sprites_visiveis, self.sprites_colisao], 'grama', grama_random)
                        elif tipo == 'objetos':
                            superficie_obj = graficos['objetos'][int(valor)]
                            Ladrilho((x, y), [self.sprites_visiveis, self.sprites_colisao], 'objetos', superficie_obj)
                        elif tipo == 'inimigos':
                            if valor == '390' or valor == '391' or valor == '392' or valor == '393':
                                nome_inimigo = 'Blue'
                            enemy(nome_inimigo,(x, y), [self.sprites_visiveis], self.sprites_colisao,)

        # adiciona jogador
        self.jogador = Jogador((2000, 1350), [self.sprites_visiveis], self.sprites_colisao)                        
    
    def run(self):
        # atualiza e desenha o mapa
        self.sprites_visiveis.desenhar_com_camera(self.jogador)
        self.sprites_visiveis.update()
        self.sprites_visiveis.enemy_update(self.jogador)


class GrupoCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.superficie_display = pygame.display.get_surface()
        self.metade_largura = self.superficie_display.get_size()[0] // 2
        self.metade_altura = self.superficie_display.get_size()[1] // 2
        self.deslocamento = pygame.math.Vector2(100, 200)
    
        # chão do cenário
        self.superficie_chao = pygame.image.load('graficos/componentes_mapa/ground.png').convert()
        self.rect_chao = self.superficie_chao.get_rect(topleft=(0, 0))

    def desenhar_com_camera(self, jogador):
        # ajusta deslocamento da câmera
        self.deslocamento.x = jogador.rect.centerx - self.metade_largura
        self.deslocamento.y = jogador.rect.centery - self.metade_altura
        
        # desenha chão
        pos_chao = self.rect_chao.topleft - self.deslocamento
        self.superficie_display.blit(self.superficie_chao, pos_chao)

        # desenha sprites na ordem Y
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            pos_sprite = sprite.rect.topleft - self.deslocamento
            self.superficie_display.blit(sprite.image, pos_sprite)

    def enemy_update(self,player):
        inimigo_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'inimigo']
        for inimigo in inimigo_sprites:
            inimigo.enemy_update(player)
