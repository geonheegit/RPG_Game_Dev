import pygame

class Map(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("map/testmap.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (3200, 3200))
        self.rect = self.image.get_rect()