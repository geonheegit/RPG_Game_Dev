import pygame
from settings import *

class Tree(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		self.image = pygame.image.load("graphics/test/blue_big_tree.png").convert_alpha()
		self.image_size = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (self.image_size[0] * 2, self.image_size[1] * 2))
		self.rect = self.image.get_rect(center = pos)
		self.hitbox = self.rect.inflate(-120, -180)