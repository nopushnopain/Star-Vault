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
        
        #Musica coletavel
        self.musica_coletavel = pygame.mixer.Sound(r"assets/coletou.wav")
        self.musica_coletavel.set_volume(0.3)

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

    def mostrar_game_over(self):
        tocar_musica('assets/game_over_sound.mp3', volume=0.5, loop=-1)
        
       
        fonte_titulo = pygame.font.SysFont('Comic Sans MS', 70, bold=True)
        fonte_opcao = pygame.font.SysFont('Comic Sans MS', 40)
        
        opcoes = ["Voltar ao Menu", "Sair"]
        botoes = []
        espacamento = 80 

        while True:
            self.janela.fill("black")
            texto = fonte_titulo.render("GAME OVER", True, (255, 0, 0))
            sombra = fonte_titulo.render("GAME OVER", True, (100, 0, 0))
            texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 3))

            # sombreamento do texto
            self.janela.blit(sombra, (texto_rect.x + 3, texto_rect.y + 3))
            self.janela.blit(texto, texto_rect)

            # botao arredondado
            mouse_pos = pygame.mouse.get_pos()
            botoes.clear()

            for i, opcao in enumerate(opcoes):
                y = ALTURA // 2 + i * espacamento
                texto_opcao = fonte_opcao.render(opcao, True, (255, 255, 255))
                rect_opcao = texto_opcao.get_rect(center=(LARGURA // 2, y))

                area_botao = rect_opcao.inflate(40, 20)

                if area_botao.collidepoint(mouse_pos):
                    cor_fundo = (70, 85, 110)
                    cor_texto = (0, 0, 0)
                else:
                    cor_fundo = (70, 70, 70)
                    cor_texto = (255, 255, 255)

                # Desenha retângulo arredondado para o botão
                pygame.draw.rect(self.janela, cor_fundo, area_botao, border_radius=12)

                # Renderiza o texto do botão
                texto_opcao = fonte_opcao.render(opcao, True, cor_texto)
                self.janela.blit(texto_opcao, rect_opcao)

                botoes.append((opcao.lower(), area_botao))

            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for nome_opcao, rect in botoes:
                        if rect.collidepoint(evento.pos):
                            return nome_opcao 

                        
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

                #colisao com os items - colocar em uma classe
                colisoes = pygame.sprite.spritecollide(self.jogador, self.itens, True)
                for item in colisoes:
                    self.musica_coletavel.play()
                    self.jogador.aplicar_efeito(item)
                    
                self.interface.atualizar_vida(self.jogador.vida)

                #verificar se o jogador morreu
                if self.jogador.vida <= 0:
                    acao = self.mostrar_game_over()
                    if acao == 'voltar ao menu':
                        tocar_musica('assets/musica_menu.mp3')
                        novo_jogo = Jogo()
                        novo_jogo.executar()
                        tocar_musica('assets/musica_menu.mp3')
                    elif acao == 'sair':
                        pygame.quit()
                        sys.exit()

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