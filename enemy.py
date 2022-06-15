import pygame
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups):

        #general settings
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #graphic setup
        self.image = pygame.image.load('graphics/player/custom_player/up/up_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)



