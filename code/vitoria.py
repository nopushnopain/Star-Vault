import pygame
import sys
from settings import LARGURA, ALTURA, FPS


def tocar_musica(caminho, volume=0.5):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
    
class Vitoria:
    def __init__(self, janela, relogio):
        self.janela = janela
        self.relogio = relogio

        self.fonte_titulo = pygame.font.SysFont('Comic Sans MS', 70, bold=True)
        self.fonte_opcao = pygame.font.SysFont('Comic Sans MS', 40)

        self.opcoes = ["Voltar ao Menu", "Sair"]
        self.espacamento = 80

    def mostrar(self):
        tocar_musica('assets/game_over_sound.mp3', volume=0.5)

        while True:
            self.janela.fill("black")

            # Título com sombra
            texto = self.fonte_titulo.render("Vitória", True, (255, 0, 0))
            sombra = self.fonte_titulo.render("Vitória", True, (100, 0, 0))
            texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 3))
            self.janela.blit(sombra, (texto_rect.x + 3, texto_rect.y + 3))
            self.janela.blit(texto, texto_rect)

            # Botões
            mouse_pos = pygame.mouse.get_pos()
            botoes = []

            for i, opcao in enumerate(self.opcoes):
                y = ALTURA // 2 + i * self.espacamento
                texto_opcao = self.fonte_opcao.render(opcao, True, (255, 255, 255))
                rect_opcao = texto_opcao.get_rect(center=(LARGURA // 2, y))
                area_botao = rect_opcao.inflate(40, 20)

                if area_botao.collidepoint(mouse_pos):
                    cor_fundo = (70, 85, 110)
                    cor_texto = (0, 0, 0)
                else:
                    cor_fundo = (70, 70, 70)
                    cor_texto = (255, 255, 255)

                pygame.draw.rect(self.janela, cor_fundo, area_botao, border_radius=12)
                texto_opcao = self.fonte_opcao.render(opcao, True, cor_texto)
                self.janela.blit(texto_opcao, rect_opcao)

                botoes.append((opcao.lower(), area_botao))

            pygame.display.update()
            self.relogio.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for nome_opcao, area in botoes:
                        if area.collidepoint(evento.pos):
                            return nome_opcao
