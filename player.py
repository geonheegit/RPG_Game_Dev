import pygame
import settings

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups, obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

		# 플레이어 이동
		self.direction = pygame.math.Vector2()
		self.speed = settings.PLAYER_SPEED

		self.obstacle_sprites = obstacle_sprites

	def input(self):
		key_pressed = pygame.key.get_pressed()

		if key_pressed[pygame.K_UP]:
			self.direction.y = -1
		elif key_pressed[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if key_pressed[pygame.K_LEFT]:
			self.direction.x = -1
		elif key_pressed[pygame.K_RIGHT]:
			self.direction.x = 1
		else:
			self.direction.x = 0

	def move(self, speed):
		# 대각선으로 이동할 때 속도 한계 돌파 방지
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
		
		# 충돌판정 적용 및 움직임 구현
		self.rect.x += self.direction.x * speed
		self.check_collision('horizontal')
		self.rect.y += self.direction.y * speed
		self.check_collision('vertical')

	# 충돌 판정
	def check_collision(self, direction):
		if direction == 'horizontal': # 좌우로 움직일 때 충돌 판정
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.rect):
					if self.direction.x > 0:
						self.rect.right = sprite.rect.left
					if self.direction.x < 0:
						self.rect.left = sprite.rect.right

		if direction == 'vertical': # 상하로 움직일 때 충돌 판정
			for sprite in self.obstacle_sprites:
				if sprite.rect.colliderect(self.rect):
					if self.direction.y > 0:
						self.rect.bottom = sprite.rect.top
					if self.direction.y < 0:
						self.rect.top = sprite.rect.bottom


	def update(self):
		self.input()
		self.move(self.speed)