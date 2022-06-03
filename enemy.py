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

        self.counter = 0
        self.last_change = 0

        self.dashdx = 0
        self.dashdy = 0
        self.overdash_mult = 1.5  # 대쉬를 했을 때 플레이어의 중심으로부터 얼마나 멀리 추가적으로 튕겨나가지면서 대쉬하는지의 배수
        self.dash_cooldown = 2000
        self.last_dash = 0
        self.current_dash_count = 0
        self.first_dashed = False

        self.dashtime = 350  # 대쉬하는 총 시간
        self.dashing_time_div = 50
        self.dash_time_gap = self.dashtime / self.dashing_time_div  # 대쉬 이동 사이 간격 틱

        self.hitbox = self.rect
        self.rect = self.default_image[0].get_rect(topleft = pos)

    def move_towards_player(self, player):
        now = pygame.time.get_ticks()
        dx, dy = player.rect.centerx - self.rect.x, player.rect.centery - self.rect.y
        dist = math.hypot(dx, dy)

        if dist <= 170:  # self.dash_time_gap (대쉬 이동 사이 간격 틱) * self.dashing_time_div (미세 대쉬 이동 조각 개수) = 대쉬하는 총 시간
            if not self.first_dashed:
                self.dashdx = dx * self.overdash_mult
                self.dashdy = dy * self.overdash_mult
            self.first_dashed = True

        if self.first_dashed:
            if self.current_dash_count != self.dashing_time_div:
                if now - self.last_dash > self.dash_time_gap:
                    self.last_dash = now
                    self.rect.x += self.dashdx / self.dashing_time_div  # 대쉬 순간의 적과 플레이어의 거리 / 미세 대쉬 이동 조각 개수 = 한 번의 미세 이동시 이동해야할 거리
                    self.rect.y += self.dashdy / self.dashing_time_div
                    self.current_dash_count += 1
            else:
                # 대쉬 쿨타임
                if now - self.last_change > self.dash_cooldown:
                    self.last_change = now
                    self.current_dash_count = 0
                    self.first_dashed = False

        if 300 > dist > 170 and not self.first_dashed:
            dx, dy = dx / dist, dy / dist  # Normalize.
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed


