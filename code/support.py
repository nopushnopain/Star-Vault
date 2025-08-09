from os import walk
import pygame

def import_folder(path):
    lista = []
    for _, __, imagem_arquivo in walk(path):
        
        for imagem in imagem_arquivo:
            caminho = path + '/' + imagem
            image_surf = pygame.image.load(caminho).convert_alpha()
            lista.append(image_surf)
    
    return lista