import pygame

class Map(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.zoom = 2
        self.image = pygame.image.load("map/testmap.png").convert_alpha()
        self.image_size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.image_size[0] * self.zoom, self.image_size[1] * self.zoom)) # 32픽셀맵 :1600 더블
        self.rect = self.image.get_rect()
        print(self.image.get_size())