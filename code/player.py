import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstaculo_sprite):
        super().__init__(groups) 
        self.image = pygame.image.load(r"graficos\Protagonista\Idle\2.png")
        self.rect = self.image.get_rect(topleft = pos) #rect lida com posicao e colisao de sprites
        
        self.direction = pygame.math.Vector2() #armazena as pos x,y
        self.speed = 5

        self.obstacle_sprites = obstaculo_sprite

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x*speed
        self.collision("horizontal")
        self.rect.y += self.direction.y*speed
        self.collision("vertical")
        #self.rect.center += self.direction*speed

    def collision(self, direction):
        if direction == "horizontal":
            for sprites in self.obstacle_sprites:
                if sprites.rect.colliderect(self.rect):
                    if self.direction.x > 0: #colisao ao mover para a direita
                        self.rect.right = sprites.rect.left
                    if self.direction.x < 0: #colisao ao mover para a esquerda
                        self.rect.left = sprites.rect.right
                    
        if direction == "vertical":
            for sprites in self.obstacle_sprites:
                if sprites.rect.colliderect(self.rect):
                    if self.direction.y > 0: #colisao ao mover para baixo
                        self.rect.bottom = sprites.rect.top
                    if self.direction.y < 0: #colisao ao mover para cima
                        self.rect.top = sprites.rect.bottom
    def update(self):
        self.input()
        self.move(self.speed)