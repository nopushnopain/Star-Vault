import sys
import pygame
from debug import debug  # ferramenta de depuração (não essencial)
from mapa import Mapa
from settings import *  # importa todas as configurações
import random
from consumivel import Itens  # classe para itens consumíveis
 
class Jogo:
    def __init__(self):
        # configuração inicial
        pygame.init()
        pygame.display.set_caption("Star Vault")  # título da janela
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))  # cria janela
        self.relogio = pygame.time.Clock()  # controle de FPS
        
        self.mapa_jogo = Mapa()  # inicializa o mapa
        self.jogador = self.mapa_jogo.jogador
        
        self.todos_sprites = pygame.sprite.Group()
        self.itens = pygame.sprite.Group()
        
        lista_itens = [
        ("itens/heart.png", "vida"),
        ("itens/speed.png", "velocidade"), #Lista de itens 
        ("itens/strong.png", "ataque"),
        ]
        for arquivo, tipo in lista_itens:
            for _ in range(6):  # gera 6 itens de cada tipo
                px, py = self.jogador.rect.center
                item_x = px + random.randint(-1400, 1400)
                item_y = py + random.randint(-1400, 1400)
                item = Itens(item_x, item_y, arquivo, tipo, self.mapa_jogo.sprites_visiveis, self.itens)  # cria o item e adiciona ao grupo
 
    def executar(self):
        while True:
            # processa eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:  # fechar no "X"
                    pygame.quit()
                    sys.exit()
            # colisão jogador para itens 
            colisoes = pygame.sprite.spritecollide(self.jogador, self.itens, True)
            for item in colisoes:
                self.jogador.aplicar_efeito(item)
        # colisões com itens:
            self.janela.fill('black')  # limpa tela
            self.mapa_jogo.run()  # atualiza mapa

            #debug atributos 
            debug(f"Vida: {getattr(self.jogador, 'vida', 0)}", 10, 10)
            debug(f"Ataque: {getattr(self.jogador, 'ataque', 0)}", 30, 10)
            debug(f"Velocidade: {self.jogador.velocidade}", 50, 10) 
            
            pygame.display.update()  # atualiza tela
            self.relogio.tick(FPS)  # limita FPS 
                 
if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()
