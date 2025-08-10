import pygame

pygame.init()
font = pygame.font.Font(None,30)

def debug(info, y = 10, x = 10):
    display_superficie = pygame.display.get_surface()
    debug_superf = font.render(str(info), True, 'White')
    debug_rect = debug_superf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_superficie, 'Black', debug_rect)
    display_superficie.blit(debug_superf, debug_rect)