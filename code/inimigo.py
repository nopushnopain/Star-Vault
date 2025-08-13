import pygame
from settings import *
from support import import_folder
from entidade import Entity

class enemy (Entity):
    def __init__ (self,nome,pos,groups, obstaculo_sprites):
        #
        super().__init__(groups)
        self.nome_inimigo = nome
        self.tipo_sprite = 'inimigo'
        self.status = 'idle'
        self.import_sprites_inimigo()
        self.image = self.animacoes[self.status][self.indice_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)  

        #movimento

        self.can_ataque = True
        self.atk_cooldown = 500
        self.atk_tempo = None

        self.obstacle_sprites = obstaculo_sprites

        #status
        #self.nome_inimigo = nome
        inimigo_info = monster_data[self.nome_inimigo]
        self.vida = inimigo_info['vida']
        self.dano = inimigo_info['dano']
        self.velocidade = inimigo_info['velocidade']
        self.raio_ataque = inimigo_info['raio_ataque']
        self.raio_percepcao = inimigo_info['raio_percepcao']    
    
    
    def import_sprites_inimigo(self):
        self.animacoes = {'idle':[],'move':[],'ataque':[]}
        caminho = f'graficos/inimigos/{self.nome_inimigo}/'
        for animation in self.animacoes.keys():
            self.animacoes[animation] = import_folder(caminho + animation)

    def get_jogador_distancia_direcao(self,jogador):
        inimigo_vec = pygame.math.Vector2(self.rect.center)
        jogador_vec = pygame.math.Vector2(jogador.rect.center)
        distancia = (jogador_vec - inimigo_vec).magnitude()
        
        if distancia > 0:
            direcao = (jogador_vec - inimigo_vec).normalize()
        else:
            direcao = pygame.math.Vector2()

        return (distancia, direcao)
    
    def get_status(self,jogador):
        distancia = self.get_jogador_distancia_direcao(jogador)[0]

        if distancia <= self.raio_ataque and self.can_ataque:
            if self.status != 'ataque':
                self.indice_frame = 0
            self.status = 'ataque'
        elif distancia <= self.raio_percepcao:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, jogador):
        if self.status == 'ataque':
            self.atk_tempo = pygame.time.get_ticks()

            if self.hitbox.colliderect(jogador.hitbox) and self.can_ataque:
                jogador.vida -= self.dano
                self.can_ataque = False

        elif self.status == 'move':
            self.direcao = self.get_jogador_distancia_direcao(jogador)[1]
        else:
            self.direcao = pygame.math.Vector2()


    def animate(self):
        animacao = self.animacoes[self.status]
        
        self.indice_frame += self.animation_speed
        if self.indice_frame >= len(animacao):
            if self.status == 'ataque':
                self.can_ataque = False
            self.indice_frame = 0

        self.image = animacao[int(self.indice_frame)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def cooldown(self):
        if not self.can_ataque:
            current_time = pygame.time.get_ticks()
            if current_time - self.atk_tempo >= self.atk_cooldown:
                self.can_ataque = True

    def update(self):
        self.move(self.velocidade)
        self.animate()
        self.cooldown()

    def enemy_update(self,jogador):
        self.get_status(jogador)
        self.actions(jogador)

    