import pygame
from settings import *  # noqa: F403


class Ladrilho(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, sprite_type, superficie = pygame.Surface((LADRILHOSIZE, LADRILHOSIZE))):  # noqa: F405
        super().__init__(grupos)
        self.sprite_type = sprite_type
        self.image = superficie
        if sprite_type == 'objetos':
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - LADRILHOSIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10) # pega o retangulo da imagem e muda o tamanho