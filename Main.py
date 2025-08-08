import pygame
import spritesheet 
pygame.init()

LARGURA_SCREEN = 1600
ALTURA_SCREEN = 900

screen = pygame.display.set_mode((LARGURA_SCREEN, ALTURA_SCREEN))
pygame.display.set_caption("Star Vault")

sprite_sheet_image = pygame.image.load(r"animacoes_e_fotos/Sprite.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50) #Cor de fundo
BLACK = (0, 0, 0)

#Criar lista para animação
animation_list = []
animation_steps = {"andar_direita": {"frames": 9, "linha": 11}, "andar_esquerda": {"frames": 9, "linha": 9},
                   "andar_frente": {"frames": 9, "linha": 8},"andar_tras": {"frames": 9, "linha": 10},
                    "morrer": {"frames": 6, "linha": 20}}

action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 100
step_counter = 0
x, y =0, 0
vel_movimento = 0.40

for animation in animation_steps.values():
    temp_animation_list = []
    for f in range(animation["frames"]):
        temp_animation_list.append(sprite_sheet.get_image(f, 64, 64, animation["linha"], 1.5,  BLACK))     
        step_counter += 1
    animation_list.append(temp_animation_list)  

#--------------------------RODAR------------------------------------#
run = True
while run:

    #carregar fundo
    screen.fill(BG) #Carregar cor de fundo

    #Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quando clica no x em cima sai do jogo
            run = False
            


       
    
    pygame.display.update()

pygame.quit()

