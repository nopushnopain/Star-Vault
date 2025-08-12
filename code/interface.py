import pygame

class Interface:
    def __init__(self, tela):
        self.tela = tela

        # Vida
        self.vida_max = 5
        self.vida_atual = 4
        self.coracao_img = pygame.image.load("assets/icone_vida.png").convert_alpha()
        self.coracao_img = pygame.transform.scale(self.coracao_img, (32, 32))

    def atualizar_vida(self, nova_vida):
        self.vida_atual = max(0, min(nova_vida, self.vida_max))

    def desenhar(self):
        # Desenhar corações (vida)
        for i in range(self.vida_atual):
            x = 30 + i * (self.coracao_img.get_width() + 4)
            y = 25
            self.tela.blit(self.coracao_img, (x, y))