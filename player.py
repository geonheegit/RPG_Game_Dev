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
		self.rect.center += self.direction * speed

	def update(self):
		self.input()
		self.move(self.speed)