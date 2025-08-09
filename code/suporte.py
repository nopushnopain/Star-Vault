import pygame
from csv import reader
from os import walk


def import_csv_layout(path):
    terreno_mapa = []
    with open(path) as mapa_:
        layout = reader(mapa_, delimiter = ',')
        for linha in layout:
            terreno_mapa.append(list(linha))
        return terreno_mapa
    

def importa_pasta(path):
    lista_superficie = []
    for _,__,img_files in walk(path):
        for imagem in img_files:
            full_path = path + '/' + imagem
            superficie_imagem = pygame.image.load(full_path).convert_alpha()
            lista_superficie.append(superficie_imagem)

    return lista_superficie
