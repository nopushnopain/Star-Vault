import sys
import pygame
from debug import debug  # ferramenta de depuração (não essencial)
from mapa import Mapa
from settings import *  # importa todas as configurações

class Jogo:
    def __init__(self):
        # configuração inicial
        pygame.init()
        pygame.display.set_caption("Star Vault")  # título da janela
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))  # cria janela
        self.relogio = pygame.time.Clock()  # controle de FPS
        self.mapa_jogo = Mapa()  # inicializa o mapa
        
    def executar(self):
        while True:
            # processa eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:  # fechar no "X"
                    pygame.quit()
                    sys.exit()
                    
            self.janela.fill('black')  # limpa tela
            self.mapa_jogo.run()  # atualiza mapa
            pygame.display.update()  # atualiza tela
            self.relogio.tick(FPS)  # limita FPS
        
if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()
