import pygame
from settings import *
from support import import_folder

#=======
class Jogador(pygame.sprite.Sprite):
    def __init__(self, posicao, grupos, sprites_colisao):
        super().__init__(grupos) 

        # imagem inicial (sprite base)
        self.image = pygame.image.load(r"graficos/protagonista/Idle_baixo/b44f8b4d-c668-4adf-af21-1d2e94f6e5a6.png")
        self.rect = self.image.get_rect(topleft=posicao)  # posição inicial

        # Ajusta hitbox para ficar menor, por exemplo, reduzindo largura e altura
        self.hitbox = self.rect.inflate(-60, -60)  # diminui 60px na largura e 60px na altura
               
        # animações
        self.importar_sprites_personagem()
        self.estado = "Idle_baixo"
        self.frame_indice = 0
        self.velocidade_animacao = 0.15
       
        # movimento
        self.direcao = pygame.math.Vector2()  # armazena x,y
        self.velocidade = 5
       
        # ataque
        self.atacando = False
        self.tempo_recarga_ataque = 1000  # ms
        self.tempo_inicio_ataque = None
        
        #vida
        self.vida = 4
        self.ataque = 10  # dano de ataque

        # colisões
        self.sprites_colisao = sprites_colisao

        #sons
        self.som_golpe = pygame.mixer.Sound(r"assets/sword-sound-260274.mp3")
        self.som_golpe.set_volume(0.5)

        self.debug_ataque = True

    # carrega todos os sprites do personagem para animação
    def importar_sprites_personagem(self):
        caminho_base = r"graficos/protagonista"
        self.animacoes = {
            "Andar_cima": [], "Andar_baixo": [], "Andar_esquerda": [], "Andar_direita": [],
            "Atacar_cima": [], "Atacar_baixo": [], "Atacar_esquerda": [], "Atacar_direita": [],
            "Idle_cima": [], "Idle_baixo": [], "Idle_direita": [], "Idle_esquerda": []
        }
        for nome_animacao in self.animacoes:
            caminho = f"{caminho_base}/{nome_animacao}"
            self.animacoes[nome_animacao] = import_folder(caminho, 1.5)


    # gerencia mudança de estado do personagem
    def atualizar_estado(self):
        # parado
        if self.direcao.x == 0 and self.direcao.y == 0:
            if "Idle" not in self.estado and "Atacar" not in self.estado:
                self.estado = self.estado.replace("Andar", "Idle")
            elif "Atacar" in self.estado:
                self.estado = self.estado.replace("Atacar", "Idle")

        # atacando
        if self.atacando:
            self.direcao.x = 0
            self.direcao.y = 0
            if "Atacar" not in self.estado:
                self.estado = self.estado.replace("Idle", "Atacar") if "Idle" in self.estado else self.estado.replace("Andar", "Atacar")
        else:
            if "Atacar" in self.estado:
                self.estado = self.estado.replace("Atacar_", " ")

    # captura teclas pressionadas
    def capturar_input(self):
        teclas = pygame.key.get_pressed()

        if not self.atacando:
            # movimento vertical
            if teclas[pygame.K_UP]:
                self.direcao.y = -1
                self.estado = "Andar_cima"
            elif teclas[pygame.K_DOWN]:
                self.direcao.y = 1
                self.estado = "Andar_baixo"
            else:
                self.direcao.y = 0
            
            # movimento horizontal
            if teclas[pygame.K_RIGHT]:
                self.direcao.x = 1
                self.estado = "Andar_direita"
            elif teclas[pygame.K_LEFT]:
                self.direcao.x = -1
                self.estado = "Andar_esquerda"
            else:
                self.direcao.x = 0
        
        # ataque
        if teclas[pygame.K_SPACE] and not self.atacando:
            self.atacando = True
            self.tempo_inicio_ataque = pygame.time.get_ticks()
            self.som_golpe.play()

    # gerencia tempo de recarga das ações
    def gerenciar_cooldowns(self):
        agora = pygame.time.get_ticks()
        if self.atacando and (agora - self.tempo_inicio_ataque >= self.tempo_recarga_ataque):
            self.atacando = False
    
    # move o jogador e verifica colisões
    def mover(self, velocidade):
        if self.direcao.magnitude() != 0:
            self.direcao = self.direcao.normalize()

        self.hitbox.x += self.direcao.x*velocidade
        self.verificar_colisao("horizontal")
        self.hitbox.y += self.direcao.y*velocidade
        self.verificar_colisao("vertical")

    # evita sobreposição com obstáculos
    def verificar_colisao(self, direcao):

        #Colisao com os Blocos
        if direcao == "horizontal":
            for sprites in self.sprites_colisao:
                if sprites.rect.colliderect(self.hitbox):
                    if self.direcao.x > 0: #colisao ao mover para a direita
                        self.hitbox.right = sprites.rect.left
                    if self.direcao.x < 0: #colisao ao mover para a esquerda
                        self.hitbox.left = sprites.rect.right
                    
        if direcao == "vertical":
            for sprites in self.sprites_colisao:
                if sprites.rect.colliderect(self.hitbox):
                    if self.direcao.y > 0: #colisao ao mover para baixo
                        self.hitbox.bottom = sprites.rect.top
                    if self.direcao.y < 0: #colisao ao mover para cima
       
                        self.hitbox.top = sprites.rect.bottom
    
    # Aplicação dos efeitos dos Itens 
    def aplicar_efeito(self, item):
        if item.tipo == "vida":
            self.vida += 1
        elif item.tipo == "velocidade":
            self.velocidade += 1  #balanciamento
        elif item.tipo == "ataque":
            self.ataque += 2 #balanciamento          

    #Interaçao de Ataque com inimigos
    def atacar(self, inimigos):
        if self.atacando:
            hitbox_ataque = self.hitbox.copy()

            #aumentar o range de ataque para onde o personagem olha
            if "baixo" in self.estado:
                hitbox_ataque.y += 45
            
            elif "cima" in self.estado:
                hitbox_ataque.y -= 45
            
            elif "direita" in self.estado:
                hitbox_ataque.x += 50
            
            elif "esquerda" in self.estado:
                hitbox_ataque.x -= 50
            
            hitbox_ataque.inflate_ip(20, 20) #aumentar range lateral

            for inimigo in inimigos:
                if hitbox_ataque.colliderect(inimigo.hitbox):
                    inimigo.vida -= self.ataque
                    if inimigo.vida <= 0:
                        inimigo.kill()
                    self.debug_ataque = False
  

    # controla animação do personagem
    def animar(self):
        frames = self.animacoes[self.estado]
        self.frame_indice += self.velocidade_animacao
        if self.frame_indice >= len(frames):
            if self.estado == 'Atacar':
                self.debug_ataque = False
            self.frame_indice = 0
        
        self.image = frames[int(self.frame_indice)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    # atualização por frame
    def update(self): 
        self.capturar_input()
        self.gerenciar_cooldowns()
        self.atualizar_estado()
        self.animar()
        self.mover(self.velocidade)
