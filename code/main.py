import sys
import pygame
from mapa import Mapa
from settings import *
from menu import Menu
from pause_menu import PauseMenu
from interface import Interface

def tocar_musica(caminho, volume=0.5, loop=-1):
    pygame.mixer.music.stop()  # Garante reinício
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loop)

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("Star Vault")
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        self.relogio = pygame.time.Clock()

        # Instancia menus e interface
        self.menu = Menu(self.janela, self.relogio)
        self.pause_menu = PauseMenu(self.janela, self.relogio)
        self.interface = Interface(self.janela)

        # Toca música do menu e exibe o menu inicial
        tocar_musica('assets/musica_menu.mp3')
        self.menu.mostrar_menu()

        # Se o jogador clicou em "JOGAR"
        if self.menu.estado == 'jogo':
            tocar_musica('assets/forest.mp3')
            self.mapa_jogo = Mapa()
        else:
            self.mapa_jogo = None

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    acao = self.pause_menu.mostrar_pause_menu()

                    if acao == "menu":
                        tocar_musica('assets/musica_menu.mp3')
                        self.menu.estado = "menu"
                        self.menu.mostrar_menu()

                        if self.menu.estado == 'jogo':
                            tocar_musica('assets/forest.mp3')
                            self.mapa_jogo = Mapa()
                    else:
                        pygame.mixer.music.unpause()

            if self.mapa_jogo:
                self.janela.fill('black')
                self.mapa_jogo.run()
                self.interface.desenhar()
                pygame.display.update()
                self.relogio.tick(FPS)

if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()