import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, grupos):
        super().__init__(grupos)
        self.image = pygame.image.load('graficos/test/yoda.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direcao = pygame.math.Vector2()
        self.speed = 5
        
        
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
        self.rect.center += self.direcao * speed
            
    def update(self):
        self.input()
        self.movimento(self.speed)