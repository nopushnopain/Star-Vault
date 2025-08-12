import pygame
from settings import *

class Ladrilho(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, tipo_sprite, superficie=pygame.Surface((LADRILHOSIZE, LADRILHOSIZE))):
        super().__init__(grupos)
        self.tipo_sprite = tipo_sprite
        self.image = superficie
        
        # ajusta posição dependendo do tipo
        if tipo_sprite == 'objetos':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - LADRILHOSIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        
        # hitbox reduzida
        self.hitbox = self.rect.inflate(0, -10)
