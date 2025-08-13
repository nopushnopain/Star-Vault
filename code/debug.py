import pygame

pygame.init()
font = pygame.font.Font(None,30)

def debug(info, y=10, x=1590):
    display_superficie = pygame.display.get_surface()
    debug_superf = font.render(str(info), True, 'White')
    debug_rect = debug_superf.get_rect(topright=(x, y))

    margem = 5  # margem extra para apagar sobras
    debug_rect_inflated = debug_rect.inflate(margem*2, margem*2)

    pygame.draw.rect(display_superficie, 'Black', debug_rect_inflated)
    display_superficie.blit(debug_superf, debug_rect)

