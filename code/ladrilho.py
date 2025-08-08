import pygame
from settings import *

class Ladrilho(pygame.sprite.Sprite):
    def __init__(self, pos, grupos):
        super().__init__(grupos)
        self.image = pygame.image.load('graficos/test/rocha.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)