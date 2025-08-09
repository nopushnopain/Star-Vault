import pygame
from settings import *


class Ladrilho(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, sprite_type, superficie = pygame.Surface((LADRILHOSIZE, LADRILHOSIZE))):
        super().__init__(grupos)
        self.sprite_type = sprite_type
        self.image = superficie
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10) # pega o retangulo daa imagem e muda o tamanho