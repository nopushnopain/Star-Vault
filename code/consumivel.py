import pygame
import random 
import os 
class Itens(pygame.sprite.Sprite):
    def __init__(self, x, y, arquivo_imagem, tipo, *grupos):
        super().__init__(*grupos)
        self.tipo = tipo
        self.image = pygame.image.load(arquivo_imagem).convert_alpha()
        if tipo == "ataque":
            self.image = pygame.transform.scale(self.image, (50, 50))
        else:
             self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect(topleft=(x, y))
        #drop itens 
    def drop_itens(pos_x, pos_y, grupo_itens, sprites_visiveis):
        # Define a lista de arquivos de itens
        lista_itens = [
            ("itens/heart.png", "vida"),
            ("itens/speed.png", "velocidade"),
            ("itens/strong.png", "ataque"),
        ]
        arquivo, tipo = random.choice(lista_itens)
        itens = Itens(pos_x, pos_y, arquivo, tipo, sprites_visiveis, grupo_itens)
        return itens
        
        # Seleciona um item aleatório da lista
        #arquivo, tipo = random.choice(lista_itens)
        
        # Cria o item e adiciona aos grupos
        #Itens(pos_x, pos_y, arquivo, tipo, sprites_visiveis, grupo_itens)
        

#def cria_itens_aleatorios(jogador, sprites_visiveis, grupo_itens, qntd = 6):
        #Lista de Possiveis items
        #lista_itens = [
        #("itens/heart.png", "vida"),
        #("itens/speed.png", "velocidade"),
        #("itens/strong.png", "ataque"),
        #]
        
        #jogador_x, jogador_y = jogador.rect.center
        #Gerando Items Aleatoriamente
        #for arquivo, tipo in lista_itens:
            #for _ in range(qntd):
                #item_x = jogador_x + random.randint(-1400, 1400)
                #item_y = jogador_y + random.randint(-1400, 1400)
                #Itens(item_x, item_y, arquivo, tipo, sprites_visiveis, grupo_itens)