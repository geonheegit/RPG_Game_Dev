import pygame
import math
import time

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.count_jump = 0
        self.zoom = 1
        self.speed = 3
        self.image = pygame.image.load('graphics/monsters/slime/slime.png').convert_alpha()
        self.default_image = [self.image]
        self.image_size = self.default_image[0].get_size()
        self.rect = self.image.get_rect()
        self.default_image[0] = pygame.transform.scale(self.default_image[0], (self.image_size[0] * self.zoom, self.image_size[1] * self.zoom))

        self.anim_list_move = []
        self.anim_list_idle = []
        self.frame_speed = 120

        self.counter = 0
        self.last_change = 0
        self.frame_speed = 120

        self.hitbox = self.rect
        self.rect = self.default_image[0].get_rect(topleft = pos)

    def move_towards_player(self, player):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if 400 >= dist >= 100:
            print(dist)
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        if dist <= 100:
            pass


