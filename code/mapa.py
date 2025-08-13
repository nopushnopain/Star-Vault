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

        #sprites de ataque
        self.ataque_atual = None
        self.sprite_ataque = pygame.sprite.Group() #personagem
        self.sprite_atacavel = pygame.sprite.Group() #inimigos
        
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
                for coluna_idx, coluna in enumerate(linha):
                    if coluna != '-1':
                        x = coluna_idx * LADRILHOSIZE
                        y = linha_idx  * LADRILHOSIZE

                        if tipo == 'limite':
                            Ladrilho((x, y), [self.sprites_colisao], 'invisivel')

                        if tipo == 'grama':
                            imagem_grama_random = choice(graficos['grama']) # seleciona aleatoriamente
                            Ladrilho(
                                    (x, y),
                                    [self.sprites_visiveis, self.sprites_colisao, self.sprite_atacavel],
                                    'grama',
                                    imagem_grama_random)

                        if tipo == 'objetos':
                            superficie_obj = graficos['objetos'][int(coluna)]
                            Ladrilho((x, y), [self.sprites_visiveis, self.sprites_colisao], 'objetos', superficie_obj)

                        elif tipo == 'inimigos':

                            if coluna == '390':
                                nome_inimigo = 'Blue'
                            elif coluna == '393':
                                 nome_inimigo = 'Goblin'
                            elif coluna == '392':
                                nome_inimigo = 'Lobisomem'
                            elif coluna == '391':
                                nome_inimigo = 'Minotauro'
                            elif coluna == '396':
                                nome_inimigo = 'Castor'
                            enemy(nome_inimigo,(x, y), [self.sprites_visiveis], self.sprites_colisao)


        # adiciona jogador
        self.jogador = Jogador((2000, 1350), [self.sprites_visiveis], self.sprites_colisao)                        
    
    def logica_ataca_grama(self):
        if self.jogador.atacando:
            hitbox_ataque = self.jogador.hitbox.copy()
            # Expande o retângulo de ataque
            hitbox_ataque.inflate_ip(40, 40)

            # Para cada sprite "atacável" (incluindo a grama)
            for sprite_alvo in self.sprite_atacavel:
                # Verifica se o retângulo de ataque do jogador colide com o sprite "atacável"
                if hitbox_ataque.colliderect(sprite_alvo.rect):
                    if sprite_alvo.tipo_sprite == 'grama':
                        sprite_alvo.kill()


    def run(self):
        # atualiza e desenha o mapa
        self.sprites_visiveis.desenhar_com_camera(self.jogador)
        self.sprites_visiveis.enemy_update(self.jogador)
        self.sprites_visiveis.update()
        inimigos = [sprite for sprite in self.sprites_visiveis if hasattr(sprite, 'tipo_sprite') and sprite.tipo_sprite == 'inimigo']
        self.jogador.atacar(inimigos)
        self.logica_ataca_grama()



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
        inimigo_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'tipo_sprite') and sprite.tipo_sprite == 'inimigo']
        for inimigo in inimigo_sprites:
            inimigo.enemy_update(player)
