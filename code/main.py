import sys
import pygame
from mapa import Mapa
from debug import debug
#<<<<<<< HEAD
from settings import *
from menu import Menu
from pause_menu import PauseMenu
from interface import Interface

def tocar_musica(caminho, volume=0.5, loop=-1):
    pygame.mixer.music.stop()  # Garante reinício
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loop)

from settings import *  # importa todas as configurações
import random
from consumivel import Itens  # classe para itens consumíveis
 
#>>>>>>> consumiveis
class Jogo:
    def __init__(self):
        pygame.init()
#<<<<<<< HEAD
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

#=======
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
 
#>>>>>>> consumiveis
    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
#<<<<<<< HEAD
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

#=======
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
                 
#>>>>>>> consumiveis
if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()