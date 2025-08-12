import sys
import pygame
from mapa import Mapa
from debug import debug
from settings import *
from menu import Menu
from pause_menu import PauseMenu
from interface import Interface
from consumivel import cria_itens_aleatorios

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

        # Toca música do menu e exibe o menu inicial
        tocar_musica('assets/musica_menu.mp3')
        self.menu.mostrar_menu()

        # Se o jogador clicou em "JOGAR"
        if self.menu.estado == 'jogo':
            tocar_musica('assets/forest.mp3')
            self.mapa_jogo = Mapa()
        else:
            self.mapa_jogo = None
        
        self.itens = pygame.sprite.Group()
        self.jogador = self.mapa_jogo.jogador

        # Cria os itens aleatórios no mapa, adicionando nos grupos
        cria_itens_aleatorios(self.jogador, self.mapa_jogo.sprites_visiveis, self.itens, qntd=6)

        self.interface = Interface(self.janela, self.jogador.vida)

        for item in self.itens:
            self.mapa_jogo.sprites_visiveis.add(item)



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

                #colisao com os items
                colisoes = pygame.sprite.spritecollide(self.jogador, self.itens, True)
                for item in colisoes:
                    self.jogador.aplicar_efeito(item)
                    if item.tipo == "vida":
                        self.interface.atualizar_vida(self.jogador.vida)

                #debug atributos 
                debug(f"Vida: {getattr(self.jogador, 'vida', 0)}", 10, LARGURA - 10)
                debug(f"Ataque: {getattr(self.jogador, 'ataque', 0)}", 30, LARGURA - 10)
                debug(f"Velocidade: {self.jogador.velocidade}", 50, LARGURA - 10)
                debug(f"Atacando: {self.jogador.debug_ataque}", 70, LARGURA - 10)

                
                pygame.display.update()  # atualiza tela
                self.relogio.tick(FPS)  # limita FPS 
                 
#>>>>>>> consumiveis
if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()