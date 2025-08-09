import pygame
from csv import reader
from os import walk

def import_csv_layout(caminho):
    # importa layout CSV do mapa
    layout_terreno = []
    with open(caminho) as arquivo_mapa:
        leitor = reader(arquivo_mapa, delimiter=',')
        for linha in leitor:
            layout_terreno.append(list(linha))
    return layout_terreno

def importa_pasta(caminho):
    # importa todas as imagens da pasta
    lista_superficies = []
    for _, __, arquivos_img in walk(caminho):
        for imagem in arquivos_img:
            caminho_completo = f"{caminho}/{imagem}"
            superficie_img = pygame.image.load(caminho_completo).convert_alpha()
            lista_superficies.append(superficie_img)
    return lista_superficies
