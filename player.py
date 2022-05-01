import pygame
import settings


class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups, obstacle_sprites):
		super().__init__(groups)
		# 기본
		self.zoom = 2
		self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
		self.default_image = [self.image]
		self.image_size = self.default_image[0].get_size()
		self.default_image[0] = pygame.transform.scale(self.default_image[0], (self.image_size[0] * self.zoom, self.image_size[1] * self.zoom))

		self.anim_list_up = []
		self.anim_list_down = []
		self.anim_list_left = []
		self.anim_list_right = []
		self.frame_speed = 120

		# UP
		self.image_up0 = pygame.image.load('graphics/player/up/up_0.png').convert_alpha()
		self.image_up1 = pygame.image.load('graphics/player/up/up_1.png').convert_alpha()
		self.image_up2 = pygame.image.load('graphics/player/up/up_2.png').convert_alpha()
		self.image_up3 = pygame.image.load('graphics/player/up/up_3.png').convert_alpha()
		for i in range(4):
			self.anim_list_up.append(eval("self.image_up{}".format(i)))

		# DOWN
		self.image_down0 = pygame.image.load('graphics/player/down/down_0.png').convert_alpha()
		self.image_down1 = pygame.image.load('graphics/player/down/down_1.png').convert_alpha()
		self.image_down2 = pygame.image.load('graphics/player/down/down_2.png').convert_alpha()
		self.image_down3 = pygame.image.load('graphics/player/down/down_3.png').convert_alpha()
		for i in range(4):
			self.anim_list_down.append(eval("self.image_down{}".format(i)))

		# LEFT
		self.image_left0 = pygame.image.load('graphics/player/left/left_0.png').convert_alpha()
		self.image_left1 = pygame.image.load('graphics/player/left/left_1.png').convert_alpha()
		self.image_left2 = pygame.image.load('graphics/player/left/left_2.png').convert_alpha()
		self.image_left3 = pygame.image.load('graphics/player/left/left_3.png').convert_alpha()
		for i in range(4):
			self.anim_list_left.append(eval("self.image_left{}".format(i)))

		# RIGHT
		self.image_right0 = pygame.image.load('graphics/player/right/right_0.png').convert_alpha()
		self.image_right1 = pygame.image.load('graphics/player/right/right_1.png').convert_alpha()
		self.image_right2 = pygame.image.load('graphics/player/right/right_2.png').convert_alpha()
		self.image_right3 = pygame.image.load('graphics/player/right/right_3.png').convert_alpha()
		for i in range(4):
			self.anim_list_right.append(eval("self.image_right{}".format(i)))

		self.rect = self.default_image[0].get_rect(topleft = pos) # 수정
		self.hitbox = self.rect.inflate(-15, -15)

		self.count_up = 0
		self.count_down = 0
		self.count_left = 0
		self.count_right = 0

		self.last_change = 0

		# 플레이어 이동
		self.direction = pygame.math.Vector2()
		self.speed = settings.PLAYER_SPEED

		self.obstacle_sprites = obstacle_sprites

		# 소리
		pygame.mixer.set_num_channels(8)
		self.grass_walk = pygame.mixer.Sound("sfx/ogg/grass_single.ogg")
		self.player_walk = pygame.mixer.Channel(1)

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
		
		# 충돌판정 적용 및 움직임 구현
		self.hitbox.x += self.direction.x * speed
		self.check_collision('RL')
		self.hitbox.y += self.direction.y * speed
		self.check_collision('UD')
		self.rect.center = self.hitbox.center

	# 충돌 판정
	def check_collision(self, direction):
		if direction == 'RL': # 좌우로 움직일 때 충돌 판정
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right

		if direction == 'UD': # 상하로 움직일 때 충돌 판정
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom

	def animate(self, max_frame):
		key_pressed = pygame.key.get_pressed()
		now = pygame.time.get_ticks()

		# UP 애니메이션 판정
		if key_pressed[pygame.K_UP]:
			if now - self.last_change > self.frame_speed:
				self.last_change = now
				self.count_up += 1
				self.image = self.anim_list_up[self.count_up]
			if self.count_up == max_frame:
				self.count_up = 0

		# DOWN 애니메이션 판정
		if key_pressed[pygame.K_DOWN]:
			if now - self.last_change > self.frame_speed:
				self.last_change = now
				self.count_down += 1
				self.image = self.anim_list_down[self.count_down]
			if self.count_down == max_frame:
				self.count_down = 0

		# LEFT 애니메이션 판정
		if key_pressed[pygame.K_LEFT]:
			if now - self.last_change > self.frame_speed:
				self.last_change = now
				self.count_left += 1
				self.image = self.anim_list_left[self.count_left]
			if self.count_left == max_frame:
				self.count_left = 0

		# RIGHT 애니메이션 판정
		if key_pressed[pygame.K_RIGHT]:
			if now - self.last_change > self.frame_speed:
				self.last_change = now
				self.count_right += 1
				self.image = self.anim_list_right[self.count_right]
			if self.count_right == max_frame:
				self.count_right = 0
		
		# 기본 상태 애니메이션
		if self.direction.x == 0 and self.direction.y == 0:
			self.image = self.default_image[0]

	def sound_check(self):
		if self.direction.x == 0 and self.direction.y == 0:
			self.is_moving = False
		else:
			self.is_moving = True

		if self.is_moving == True and self.player_walk.get_busy() == False:
			self.player_walk.play(self.grass_walk)

	def update(self):
		self.input()
		self.move(self.speed)
		self.animate(3)
		self.sound_check()