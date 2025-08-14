import sys
import pygame
from mapa import Mapa
from debug import debug
from settings import *
from menu import Menu
from pause_menu import PauseMenu
from interface import Interface
from consumivel import cria_itens_aleatorios
from game_over import GameOver
from vitoria import Vitoria

def tocar_musica(caminho, volume=0.5, loop=-1):
    pygame.mixer.music.stop()  # p/ reiniciar o DJ
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loop)
 
class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("As Aventuras de Ronaldinho")
        
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        self.relogio = pygame.time.Clock()
        
        # musica coletavel
        self.musica_coletavel = pygame.mixer.Sound(r"assets/coletou.wav")
        self.musica_coletavel.set_volume(0.3)

        # instancia menus e interface
        self.menu = Menu(self.janela, self.relogio)
        self.pause_menu = PauseMenu(self.janela, self.relogio)

        # toca musica do menu e exibe o menu inicial
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

        if hasattr(self.mapa_jogo, 'grupo_inimigos'):
            for inim in self.mapa_jogo.grupo_inimigos:
                inim.grupo_itens = self.itens
                inim.sprites_visiveis = self.mapa_jogo.sprites_visiveis
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

                # colisao com os items - colocar em uma classe
                for item in self.itens:
                    if self.jogador.hitbox.colliderect(item.rect):
                        self.musica_coletavel.play()
                        self.jogador.aplicar_efeito(item)
                        item.kill()
                    
                self.interface.atualizar_vida(self.jogador.vida)

                # verificar se o jogador morreu
                if self.jogador.estado == "Morte":
                    # registra o tempo da morte do jogador
                    if not hasattr(self, 'tempo_morte'):
                        self.tempo_morte = pygame.time.get_ticks()
                    
                    # espera 1.5 segundos antes de mostrar Game Over
                    elif pygame.time.get_ticks() - self.tempo_morte >= 1500:
                        game_over = GameOver(self.janela, self.relogio)
                        acao = game_over.mostrar()

                        if acao == 'voltar ao menu':
                            tocar_musica('assets/musica_menu.mp3')
                            self.menu.estado = 'menu'
                            self.menu.mostrar_menu()

                            if self.menu.estado == 'jogo':
                                tocar_musica('assets/forest.mp3')
                                novo_jogo = Jogo()
                                novo_jogo.executar()

                        elif acao == 'sair':
                            pygame.quit()
                            sys.exit()

                if self.jogador.pontos>=10:
                    vitoria = Vitoria(self.janela, self.relogio)
                    acao = vitoria.mostrar()
                    
                    if acao == 'voltar ao menu':
                        tocar_musica('assets/musica_menu.mp3')
                        self.menu.estado = 'menu'
                        self.menu.mostrar_menu()

                    if self.menu.estado == 'jogo':
                        tocar_musica('assets/forest.mp3')
                        novo_jogo = Jogo()
                        novo_jogo.executar()

                    elif acao == 'sair':
                        pygame.quit()
                        sys.exit()
                    # pygame.quit()
                    # sys.exit()

                #debug atributos 
                debug(f"Vida: {getattr(self.jogador, 'vida', 0)}", 10, LARGURA - 10)
                debug(f"Ataque: {getattr(self.jogador, 'ataque', 0)}", 30, LARGURA - 10)
                debug(f"Velocidade: {self.jogador.velocidade}", 50, LARGURA - 10)

                
                pygame.display.update()  # atualiza tela
                self.relogio.tick(FPS)  # limita FPS 
                 
#>>>>>>> consumiveis
if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()