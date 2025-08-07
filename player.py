import pygame
from spritesheet import SpriteSheet

class Player():
    def __init__(self, x, y, largura_tela, altura_tela, escala):
        self.x = x
        self.y = y
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.velocidade = 0.40
        self.mover = False
        self.acao = 0


        self.spritesheet = SpriteSheet()
        self.animacao_lista = []

    def movimento(self):
        pressionada = pygame.key.get_pressed()
        if pressionada[pygame.K_RIGHT]:
            self.acao = 0  # andar direita
            if x + self.velocidade + 100 <= self.largura_tela: 
                x += self.velocidade
                self.mover = True    
            else:
                self.mover = False

        elif pressionada[pygame.K_LEFT]:
            self.acao = 1  # andar esquerda
            if x + self.velocidade - 100 <= 0: 
                x -= self.velocidade
                self.mover = True    
            else:
                self.mover = False
            
        elif pressionada[pygame.K_UP]:
            self.acao = 2
            if y - self.velocidade - 100 <= 0: 
                y -= self.velocidade
                self.mover = True    
            else:
                self.mover = False
            
        elif pressionada[pygame.K_DOWN]:
            self.acao = 3  # andar tras
            if y + self.velocidade + 100 <= self.altura_tela: 
                y += self.velocidade
                self.mover = True    
            else:
                self.mover = False
            
        elif pressionada[pygame.K_SPACE]:
            self.acao = 4  # morrer
            self.mover = True
    
    def atualizar_sprite(self):
        