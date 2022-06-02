import pygame
import settings


class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups, obstacle_sprites):
		super().__init__(groups)
		# 기본
		self.zoom = 2
		self.image = pygame.image.load('graphics/player/custom_player/default/player.png').convert_alpha()
		self.default_image = [self.image]
		self.image_size = self.default_image[0].get_size()
		self.default_image[0] = pygame.transform.scale(self.default_image[0], (self.image_size[0] * self.zoom, self.image_size[1] * self.zoom))

		self.anim_list_up = []
		self.anim_list_down = []
		self.anim_list_left = []
		self.anim_list_right = []
		self.anim_list_idle = []
		self.frame_speed = 120

		# UP
		self.image_up0 = pygame.image.load('graphics/player/up/up_0.png').convert_alpha()
		self.image_up1 = pygame.image.load('graphics/player/up/up_1.png').convert_alpha()
		self.image_up2 = pygame.image.load('graphics/player/up/up_2.png').convert_alpha()
		self.image_up3 = pygame.image.load('graphics/player/up/up_3.png').convert_alpha()
		for i in range(4):
			self.anim_list_up.append(eval("self.image_up{}".format(i)))
		self.image_size_up = self.anim_list_up[0].get_size()
		for i in range(4):
			self.anim_list_up[i] = pygame.transform.scale(self.anim_list_up[i], (self.image_size_up[0] * self.zoom, self.image_size_up[1] * self.zoom))

		# DOWN
		self.image_down0 = pygame.image.load('graphics/player/down/down_0.png').convert_alpha()
		self.image_down1 = pygame.image.load('graphics/player/down/down_1.png').convert_alpha()
		self.image_down2 = pygame.image.load('graphics/player/down/down_2.png').convert_alpha()
		self.image_down3 = pygame.image.load('graphics/player/down/down_3.png').convert_alpha()
		for i in range(4):
			self.anim_list_down.append(eval("self.image_down{}".format(i)))
		self.image_size_down = self.anim_list_down[0].get_size()
		for i in range(4):
			self.anim_list_down[i] = pygame.transform.scale(self.anim_list_down[i], (self.image_size_down[0] * self.zoom, self.image_size_down[1] * self.zoom))

		# LEFT
		self.image_left0 = pygame.image.load('graphics/player/left/left_0.png').convert_alpha()
		self.image_left1 = pygame.image.load('graphics/player/left/left_1.png').convert_alpha()
		self.image_left2 = pygame.image.load('graphics/player/left/left_2.png').convert_alpha()
		self.image_left3 = pygame.image.load('graphics/player/left/left_3.png').convert_alpha()
		for i in range(4):
			self.anim_list_left.append(eval("self.image_left{}".format(i)))
		self.image_size_left = self.anim_list_left[0].get_size()
		for i in range(4):
			self.anim_list_left[i] = pygame.transform.scale(self.anim_list_left[i], (self.image_size_left[0] * self.zoom, self.image_size_left[1] * self.zoom))

		# RIGHT
		self.image_right0 = pygame.image.load('graphics/player/right/right_0.png').convert_alpha()
		self.image_right1 = pygame.image.load('graphics/player/right/right_1.png').convert_alpha()
		self.image_right2 = pygame.image.load('graphics/player/right/right_2.png').convert_alpha()
		self.image_right3 = pygame.image.load('graphics/player/right/right_3.png').convert_alpha()
		for i in range(4):
			self.anim_list_right.append(eval("self.image_right{}".format(i)))
		self.image_size_right = self.anim_list_right[0].get_size()
		for i in range(4):
			self.anim_list_right[i] = pygame.transform.scale(self.anim_list_right[i], (self.image_size_right[0] * self.zoom, self.image_size_right[1] * self.zoom))

		# IDLE
		self.image_idle0 = pygame.image.load('graphics/player/custom_player/idle/idle_0.png').convert_alpha()
		self.image_idle1 = pygame.image.load('graphics/player/custom_player/idle/idle_0.png').convert_alpha()
		self.image_idle2 = pygame.image.load('graphics/player/custom_player/idle/idle_1.png').convert_alpha()
		self.image_idle3 = pygame.image.load('graphics/player/custom_player/idle/idle_1.png').convert_alpha()
		for i in range(4):
			self.anim_list_idle.append(eval("self.image_idle{}".format(i)))
		self.image_size_idle = self.anim_list_idle[0].get_size()
		for i in range(4):
			self.anim_list_idle[i] = pygame.transform.scale(self.anim_list_idle[i], (self.image_size_idle[0] * self.zoom, self.image_size_idle[1] * self.zoom))

		self.rect = self.default_image[0].get_rect(topleft = pos) # 수정
		self.hitbox = self.rect.inflate(-15, -15)

		self.count_up = 0
		self.count_down = 0
		self.count_left = 0
		self.count_right = 0
		self.count_idle = 0

		self.last_change = 0

		# 플레이어 이동
		self.direction = pygame.math.Vector2()
		self.speed = settings.PLAYER_SPEED

		self.obstacle_sprites = obstacle_sprites

		# 동굴
		self.is_cave = True

		# 소리
		pygame.mixer.set_num_channels(8) # 소리 채널 8개로 나눠놓기

		# 걷는 소리
		self.grass_walk = pygame.mixer.Sound("sfx/ogg/grass_single.ogg")
		self.grass_walk.set_volume(0.3)
		self.player_walk = pygame.mixer.Channel(1) # player_walk 채널을 1번 채널로 설정 (grass_walk를 player_walk 채널에서 재생)

		# 동굴 BGM
		self.cave_bgm = pygame.mixer.Sound("sfx/ogg/cave_bgm.ogg")
		self.cave_bgm.set_volume(0.15)
		self.main_bgm = pygame.mixer.Channel(2) # main_bgm 채널을 2번 채널로 설정 (cave_bgm을 main_bgm 채널에서 재생)


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
		
		# IDLE 애니메이션
		if self.direction.x == 0 and self.direction.y == 0:
			if now - self.last_change > self.frame_speed:
				self.last_change = now
				self.count_idle += 1
				self.image = self.anim_list_idle[self.count_idle]
			if self.count_idle == max_frame:
				self.count_idle = 0

	def walk_sound_check(self):
		if self.direction.x == 0 and self.direction.y == 0:
			self.is_moving = False
		else:
			self.is_moving = True

		if self.is_moving and self.player_walk.get_busy() == False:  # 중복 재생 방지
			self.player_walk.play(self.grass_walk)

	def bgm_play(self):
		if not self.main_bgm.get_busy() and self.is_cave:  # 중복 재생 방지
			self.main_bgm.play(self.cave_bgm)

	def update(self):
		self.input()
		self.move(self.speed)
		self.animate(3)
		self.walk_sound_check()
		self.bgm_play()