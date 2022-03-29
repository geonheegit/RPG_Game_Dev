import pygame 
from settings import *
from tile import Tile
from player import Player


class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# 스프라이트 그룹 나누기
		self.visible_sprites = pygame.sprite.Group()
		self.obstacle_sprites = pygame.sprite.Group()

		# 맵 로딩
		self.create_map()

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Tile((x,y),[self.visible_sprites, self.obstacle_sprites]) # visible_sprites & obstacle_sprites에 포함
				if col == 'p':
					Player((x,y),[self.visible_sprites], self.obstacle_sprites) # visible_sprites에 포함 / obstacle_sprites 그룹 제공

	def run(self): # main에서 무한 반복
		# 화면에 출력
		self.visible_sprites.draw(self.display_surface) # visible_sprites에 있는 것을 화면에 출력
		self.visible_sprites.update()