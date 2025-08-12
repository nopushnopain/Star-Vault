import pygame
import sys
from settings import *

class Menu:
    def __init__(self, janela, relogio):
        self.janela = janela
        self.relogio = relogio
        self.estado = 'menu'

        # Carrega imagem de fundo
        self.bg = pygame.image.load('assets/background_menu.png').convert()
        self.bg = pygame.transform.scale(self.bg, (LARGURA, ALTURA))

        # Fontes
        self.fonte_titulo = pygame.font.SysFont(None, 120, bold=True)
        self.fonte_opcoes = pygame.font.SysFont(None, 60, bold=True)

    def desenhar_texto_menu(self, texto, cor, x, y, fonte, sombra=False):
        if sombra:
            sombra_surface = fonte.render(texto, True, (0, 0, 0))
            sombra_rect = sombra_surface.get_rect(center=(x + 3, y + 3))
            self.janela.blit(sombra_surface, sombra_rect)
        superficie = fonte.render(texto, True, cor)
        ret = superficie.get_rect(center=(x, y))
        self.janela.blit(superficie, ret)
        return ret

    def desenhar_botao_menu(self, texto, y, cor_fundo, cor_texto):
        largura = 250
        altura = 50
        x = LARGURA // 2 - largura // 2
        rect = pygame.Rect(x, y, largura, altura)

        # Sombra do botão
        sombra_rect = pygame.Rect(rect.x + 5, rect.y + 5, largura, altura)
        pygame.draw.rect(self.janela, (0, 0, 0), sombra_rect, border_radius=12)

        # Botão
        pygame.draw.rect(self.janela, cor_fundo, rect, border_radius=12)
        pygame.draw.rect(self.janela, (255, 255, 255), rect, 3, border_radius=12)

        # Texto
        self.desenhar_texto_menu(texto, cor_texto, rect.centerx, rect.centery, self.fonte_opcoes, sombra=True)
        return rect

    def mostrar_menu(self):
        while self.estado == 'menu':
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    pos_mouse = pygame.mouse.get_pos()
                    if self.btn_jogar.collidepoint(pos_mouse):
                        self.estado = 'jogo'
                    elif self.btn_sair.collidepoint(pos_mouse):
                        pygame.quit()
                        sys.exit()

            self.janela.blit(self.bg, (0, 0))

            # Título
            self.desenhar_texto_menu("STAR VOULT", (255, 215, 0), LARGURA // 2, ALTURA // 4, self.fonte_titulo, sombra=True)

            # Botões
            self.btn_jogar = self.desenhar_botao_menu("JOGAR", ALTURA // 2 - 50, (50, 150, 50), (255, 255, 255))
            self.btn_sair = self.desenhar_botao_menu("SAIR", ALTURA // 2 + 50, (150, 50, 50), (255, 255, 255))

            pygame.display.update()
            self.relogio.tick(FPS)