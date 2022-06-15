import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        # 대각선으로 이동할 때 속도 한계 돌파 방지
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # 충돌판정 적용 및 움직임 구현
        self.hitbox.x += self.direction.x * speed
        self.check_collision('RL')
        self.hitbox.y += self.direction.y * speed
        self.check_collision('UD')
        self.rect.center = self.hitbox.center


    def check_collision(self, direction):
        if direction == 'RL':  # 좌우로 움직일 때 충돌 판정
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'UD':  # 상하로 움직일 때 충돌 판정
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
