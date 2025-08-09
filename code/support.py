from os import walk
import pygame

def import_folder(path, escala = None):
    lista = []
    for _, __, imagem_arquivo in walk(path):
        
        for imagem in imagem_arquivo:
            caminho = path + '/' + imagem
            image_surf = pygame.image.load(caminho).convert_alpha()
            
            if escala:
                largura = image_surf.get_width()
                altura = image_surf.get_height()
                image_surf = pygame.transform.scale(image_surf,(int(largura * escala), int(altura * escala)))

            lista.append(image_surf)

    return lista