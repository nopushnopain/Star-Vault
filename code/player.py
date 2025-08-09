import pygame
from settings import *

class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, sprites_colisao):
        super().__init__(grupos)
        self.image = pygame.image.load('graficos/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        self.direcao = pygame.math.Vector2()
        self.velocidade = 5
        self.sprites_colisao = sprites_colisao
        
    def capturar_input(self):
        teclas = pygame.key.get_pressed()
        
        # movimento vertical
        if teclas[pygame.K_UP]:
            self.direcao.y = -1
        elif teclas[pygame.K_DOWN]:
            self.direcao.y = 1
        else:
            self.direcao.y = 0
            
        # movimento horizontal
        if teclas[pygame.K_RIGHT]:
            self.direcao.x = 1
        elif teclas[pygame.K_LEFT]:
            self.direcao.x = -1
        else:
            self.direcao.x = 0
    
    def mover(self, velocidade):
        if self.direcao.magnitude() != 0:
            self.direcao = self.direcao.normalize()
            
        # movimento horizontal
        self.hitbox.x += self.direcao.x * velocidade
        self.verificar_colisao('horizontal')
        
        # movimento vertical
        self.hitbox.y += self.direcao.y * velocidade
        self.verificar_colisao('vertical')
        
        # atualiza posição real
        self.rect.center = self.hitbox.center
            
    def verificar_colisao(self, direcao):
        for sprite in self.sprites_colisao:
            if sprite.hitbox.colliderect(self.hitbox):
                if direcao == 'horizontal':
                    if self.direcao.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direcao.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                elif direcao == 'vertical':
                    if self.direcao.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direcao.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
    
    def update(self):
        self.capturar_input()
        self.mover(self.velocidade)
