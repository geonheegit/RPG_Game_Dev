import pygame
import settings

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load('C:/Users/gram/PycharmProjects/test_game/graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

		# 추가
		self.direction = pygame.math.Vector2()
		self.speed = settings.PLAYER_SPEED

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
			
		self.rect.center += self.direction * speed

	def update(self):
		self.input()
		self.move(self.speed)