import pygame
from settings import *

class PauseMenu:
        def __init__(self, janela, relogio):
            self.janela = janela
            self.relogio = relogio
            self.font_titulo = pygame.font.SysFont("georgia", 60, bold=True)
            self.font_opcao = pygame.font.SysFont("arial", 40)

            self.opcoes = ["Retomar", "Menu Principal", "Sair"]
            self.opcao_selecionada = 0

        def mostrar_pause_menu(self):
            rodando = True

            while rodando:
                self.janela.fill((0, 0, 0))

                # Desenha o título
                titulo = self.font_titulo.render("Pausa", True, (255, 255, 255))
                self.janela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

                # Lista que armazena os retângulos das opções
                opcoes_rects = []

                # Desenha as opções
                for i, texto in enumerate(self.opcoes):
                    cor = (255, 255, 0) if i == self.opcao_selecionada else (200, 200, 200)
                    opcao_render = self.font_opcao.render(texto, True, cor)
                    rect = opcao_render.get_rect(center=(LARGURA // 2, 250 + i * 60))
                    self.janela.blit(opcao_render, rect)
                    opcoes_rects.append(rect)

                # Eventos
                for evento in pygame.event.get():

                    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        pos_mouse = pygame.mouse.get_pos()
                        for i, rect in enumerate(opcoes_rects):
                            if rect.collidepoint(pos_mouse):
                                escolha = self.opcoes[i]
                                if escolha == "Retomar":
                                    return None
                                elif escolha == "Menu Principal":
                                    return "menu"
                                elif escolha == "Sair":
                                    pygame.quit()
                                    exit()

                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            return None
                        elif evento.key == pygame.K_UP:
                            self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes)
                        elif evento.key == pygame.K_DOWN:
                            self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes)
                        elif evento.key == pygame.K_RETURN:
                            escolha = self.opcoes[self.opcao_selecionada]
                            if escolha == "Retomar":
                                return None
                            elif escolha == "Menu Principal":
                                return "menu"
                            elif escolha == "Sair":
                                pygame.quit()
                                exit()

                pygame.display.flip()
                self.relogio.tick(30)