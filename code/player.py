import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstaculo_sprite):
        super().__init__(groups) 
        self.image = pygame.image.load(r"graficos\Protagonista\Idle_baixo\a09ee047-069d-405f-8f4f-4f1c36b4d10a.png")
        self.rect = self.image.get_rect(topleft = pos) #rect lida com posicao e colisao de sprites
        #graficos
        self.import_player_assets()
        self.status = "Idle_baixo"
        self.indice_frame = 0
        self.animation_speed = 0.17
        #movimento
        self.direction = pygame.math.Vector2() #armazena as pos x,y
        self.speed = 5
        self.atacando = False
        self.atk_cooldown = 500
        self.atk_tempo = None

        self.obstacle_sprites = obstaculo_sprite

    def import_player_assets(self):
        caminho_protag = r"C:\Users\lucia\OneDrive\Área de Trabalho\Luciano\Github\Star-Vault\graficos\Protagonista"

        self.animacoes = {"Andar_cima": [], "Andar_baixo": [], "Andar_esquerda": [], "Andar_direita": [],
                          "Atacar_cima": [], "Atacar_baixo": [], "Atacar_esquerda": [], "Atacar_direita": [],
                          "Idle_cima": [], "Idle_baixo": [], "Idle_direita": [], "Idle_esquerda": []}

        for animacao in self.animacoes.keys():
            caminho = caminho_protag + "/" + animacao
            self.animacoes[animacao] = import_folder(caminho, 1.5)

    def get_status(self):

        #idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not "Idle" in self.status:
                if not "Atacar" in self.status:
                    self.status = self.status.replace("Andar", "Idle")
                else:
                    self.status = self.status.replace("Atacar", "Idle")
        #Ataque
        if self.atacando == True:
            self.direction.x = 0
            self.direction.y = 0
            if not "Atacar" in self.status:
                if "Idle" in self.status:
                    self.status = self.status.replace("Idle", "Atacar")
                elif "Andar" in self.status:
                    self.status = self.status.replace("Andar", "Atacar")   

        else:
            if "Atacar" in self.status:
             self.status = self.status.replace("Atacar_", " ")     

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.atacando:
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "Andar_cima"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "Andar_baixo"
            else:
                self.direction.y = 0
            
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "Andar_direita"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "Andar_esquerda"
            else:
                self.direction.x = 0
        
        #ataque
        if keys[pygame.K_SPACE] and self.atacando == False:
            self.atacando = True
            self.atk_tempo = pygame.time.get_ticks()
            print("Ataque")

    def cooldowns(self):
        tempo_atual = pygame.time.get_ticks()

        if self.atacando:
            if tempo_atual - self.atk_tempo >= self.atk_cooldown:
                self.atacando = False   

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x*speed
        self.collision("horizontal")
        self.rect.y += self.direction.y*speed
        self.collision("vertical")

    def collision(self, direction):
        if direction == "horizontal":
            for sprites in self.obstacle_sprites:
                if sprites.rect.colliderect(self.rect):
                    if self.direction.x > 0: #colisao ao mover para a direita
                        self.rect.right = sprites.rect.left
                    if self.direction.x < 0: #colisao ao mover para a esquerda
                        self.rect.left = sprites.rect.right
                    
        if direction == "vertical":
            for sprites in self.obstacle_sprites:
                if sprites.rect.colliderect(self.rect):
                    if self.direction.y > 0: #colisao ao mover para baixo
                        self.rect.bottom = sprites.rect.top
                    if self.direction.y < 0: #colisao ao mover para cima
                        self.rect.top = sprites.rect.bottom

    def animate(self):
        animacao = self.animacoes[self.status]

        #loop pelo indice de frame
        self.indice_frame += self.animation_speed
        if self.indice_frame >= len(animacao):
            self.indice_frame = 0
        
        # guardar posição atual antes de trocar a imagem
        centro_atual = self.rect.center

        #setar imagem
        self.image = animacao[int(self.indice_frame)]
        self.rect = self.image.get_rect(center = centro_atual)


    def update(self): 
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)