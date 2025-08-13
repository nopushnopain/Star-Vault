import pygame
import random 
class Itens(pygame.sprite.Sprite):
    def __init__(self, x, y, arquivo_imagem, tipo, *grupos):
        super().__init__(*grupos)
        self.tipo = tipo
        self.image = pygame.image.load(arquivo_imagem).convert_alpha()
        if tipo == "ataque":
            self.image = pygame.transform.scale(self.image, (50, 50))
        else:
             self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect(topleft=(x, y))
 
def cria_itens_aleatorios(jogador, sprites_visiveis, grupo_itens, qntd = 5):
        #Lista de Possiveis items
        lista_itens = [
        ("itens/heart.png", "vida"),
        ("itens/speed.png", "velocidade"),
        ("itens/strong.png", "ataque"),
        ]
        # Lista de coordenadas fixas seguras (evitando 100px das bordas)
        locais_fixos = [
            (jogador.rect.centerx + 661, jogador.rect.centery + 1367),
            (jogador.rect.centerx - 954, jogador.rect.centery - 250),
            (jogador.rect.centerx + 626, jogador.rect.centery - 500),
            (jogador.rect.centerx - 650, jogador.rect.centery + 329),
            (jogador.rect.centerx - 1119, jogador.rect.centery + 91),
            (jogador.rect.centerx - 545, jogador.rect.centery - 999),
            (jogador.rect.centerx + 535, jogador.rect.centery + 661),
            (jogador.rect.centerx - 1089, jogador.rect.centery - 400),
            (jogador.rect.centerx - 520, jogador.rect.centery + 871),
            (jogador.rect.centerx - 1226, jogador.rect.centery - 207),
            (jogador.rect.centerx + 912, jogador.rect.centery + 220),
            (jogador.rect.centerx - 566, jogador.rect.centery - 931),
            (jogador.rect.centerx - 150 , jogador.rect.centery + 500),
            (jogador.rect.centerx - 800, jogador.rect.centery + 550),
            (jogador.rect.centerx + 300, jogador.rect.centery - 800)
            
        ]
        for x, y in locais_fixos:
            arquivo, tipo = random.choice(lista_itens)  # Escolhe um aleatório para cada posição
            Itens(x, y, arquivo, tipo, sprites_visiveis, grupo_itens)
