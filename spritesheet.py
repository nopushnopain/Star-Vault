import pygame

class SpriteSheet():
    def __init__(self, imagem):
        self.sheet = imagem


    def get_image(self, frame, largura, altura, linha, escala, cor):
        imagem = pygame.Surface((largura, altura)).convert_alpha()
        imagem.blit(self.sheet, (0, 0), ((frame*largura), linha*altura, largura, altura))
        imagem = pygame.transform.scale(imagem, (largura * escala, altura * escala))
        imagem.set_colorkey(cor)

        return imagem