import pygame
from spritesheet import SpriteSheet

class Player():
    def __init__(self, x, y, escala):
        self.x = x
        self.y = y
        self.velocidade = 0.40
        self.mover = False
        self.acao = 0

        self.spritesheet = SpriteSheet()
        self.animacao_lista = []
        animation_steps = {"andar_direita": {"frames": 9, "linha": 11}, "andar_esquerda": {"frames": 9, "linha": 9},
                   "andar_frente": {"frames": 9, "linha": 8},"andar_tras": {"frames": 9, "linha": 10},
                    "morrer": {"frames": 6, "linha": 20}}

    

    def movimento(self):
        pressionada = pygame.key.get_pressed()
        if pressionada[pygame.K_RIGHT]:
            self.acao = 0  # andar direita
            if x + self.velocidade + 100 <= LARGURA_SCREEN:  # 64 é a largura do sprite
                x += self.velocidade
                self.mover = True    
            else:
                self.mover = False
        elif pressionada[pygame.K_LEFT]:
            self.acao = 1  # andar esquerda
            x -= self.velocidade
            self.mover = True
        elif pressionada[pygame.K_UP]:
            self.acao = 2  # andar frente
            y -= self.velocidade
            self.mover = True
        elif pressionada[pygame.K_DOWN]:
            self.acao = 3  # andar tras
            y += self.velocidade
            self.mover = True
        elif pressionada[pygame.K_SPACE]:
            self.acao = 4  # morrer
            self.mover = True
    
    def atualizar_sprite(self):
