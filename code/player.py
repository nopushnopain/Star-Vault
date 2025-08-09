import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, sprites_obstaculos):
        super().__init__(grupos)
        self.image = pygame.image.load('graficos/test/yoda.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        
        self.direcao = pygame.math.Vector2()
        self.speed = 5
        
        self.sprites_obstaculos = sprites_obstaculos
        
    def input(self):
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_UP]:
            self.direcao.y = -1
        elif teclas[pygame.K_DOWN]:
            self.direcao.y = 1
        else:
            self.direcao.y = 0
            
        if teclas[pygame.K_RIGHT]:
            self.direcao.x = 1
        elif teclas[pygame.K_LEFT]:
            self.direcao.x = -1
        else:
            self.direcao.x = 0
    
    def movimento(self, speed):
        if self.direcao.magnitude() != 0:
            self.direcao = self.direcao.normalize()
            
        self.hitbox.x += self.direcao.x * speed
        self.colisao('horizontal')
        self.hitbox.y += self.direcao.y * speed
        self.colisao('vertical')
        self.rect.center = self.hitbox.center
            
    def colisao(self, direcao):
        if direcao == 'horizontal':
            for sprite in self.sprites_obstaculos:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direcao.x > 0: # movendo p/ direita
                        self.hitbox.right = sprite.hitbox.left
                    if self.direcao.x < 0: # movendo p/ esquerda
                        self.hitbox.left = sprite.hitbox.right
        if direcao == 'vertical':
            for sprite in self.sprites_obstaculos:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direcao.y > 0: # movendo p/ baixo
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direcao.y < 0: # movendo p/ cima
                        self.hitbox.top = sprite.hitbox.bottom
    
    def update(self):
        self.input()
        self.movimento(self.speed)