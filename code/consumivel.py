import pygame
class Itens(pygame.sprite.Sprite):
    def __init__(self, x, y, arquivo_imagem, tipo, *grupos):
        super().__init__(*grupos)
        self.tipo = tipo
        self.image = pygame.image.load(arquivo_imagem).convert_alpha()
        self.iamge = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))