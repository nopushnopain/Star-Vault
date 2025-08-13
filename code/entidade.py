import pygame

class Entity(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.indice_frame = 0
		self.animation_speed = 0.15
		self.direcao = pygame.math.Vector2()

	def move(self,speed):
		if self.direcao.magnitude() != 0:
			self.direcao = self.direcao.normalize()

		self.hitbox.x += self.direcao.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direcao.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self,direcao):
		if direcao == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direcao.x > 0: # mover para a direita
						self.hitbox.right = sprite.hitbox.left
					if self.direcao.x < 0: # mover para a esquerda
						self.hitbox.left = sprite.hitbox.right

		if direcao == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direcao.y > 0: # mover para baixo
						self.hitbox.bottom = sprite.hitbox.top
					if self.direcao.y < 0: # mover para cima
						self.hitbox.top = sprite.hitbox.bottom