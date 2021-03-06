import pygame, sys
from settings import *
from level import Level
from csv_read import *
import tile

pygame.init()
pygame.display.set_caption('Adventure & Puzzle')
clock = pygame.time.Clock()
font = pygame.font.Font("font/Infinite Darkness.ttf",22)

screen = pygame.display.set_mode((WIDTH, HEIGTH))

def update_position():
    # 플레이어 위치 표시
    screen.blit(font.render("x: " + str(level.player.hitbox.x), 1,
                            pygame.Color("black")), (10, 30))
    screen.blit(font.render("y: " + str(level.player.hitbox.y), 1,
                            pygame.Color("black")), (10, 60))

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render("FPS: " + fps, 1, pygame.Color("white"))
    return fps_text

class GameState():
    def __init__(self):
        self.is_intro = True
        self.is_island = False
        self.is_cave = False
        self.zoom = 2
        self.STAGE = 'intro'

        # ============================ 소리 ===============================
        # 소리 채널
        pygame.mixer.set_num_channels(8)  # 소리 채널 8개로 나눠놓기

        # 동굴 BGM
        self.cave_bgm = pygame.mixer.Sound("sfx/ogg/cave_bgm.ogg")
        self.cave_bgm.set_volume(0.1)
        self.cave_bgm_chan = pygame.mixer.Channel(2)  # main_bgm 채널을 2번 채널로 설정 (cave_bgm을 main_bgm 채널에서 재생)

        # 무인도 BGM
        self.island_bgm = pygame.mixer.Sound("sfx/ogg/island_bgm.ogg")
        self.island_bgm.set_volume(0.15)
        self.island_bgm_chan = pygame.mixer.Channel(3)

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.STAGE = 'island'
                    level.current_stage = 'island'
                if event.key == pygame.K_b:
                    self.STAGE = 'cave'
                    level.current_stage = 'cave'

        if self.is_intro == False:
            level.player.hitbox.x = 0
            level.player.hitbox.y = 0
            self.is_intro = True
            self.is_island = False
            self.is_cave = False

        screen.blit(font.render("Press \'A\' to island \n Press \'B\' to test", 1,
                                pygame.Color("white")), (WIDTH / 2 - 100, HEIGTH / 2))

    def island(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.STAGE = 'island'
                    level.current_stage = 'island'

                if event.key == pygame.K_b:
                    self.STAGE = 'cave'
                    level.current_stage = 'cave'

        if self.is_island == False:
            # 맵 재로딩
            level.create_map()
            # 맵 구성 요소
            level.visible_sprites.floor_surf = pygame.image.load("map/island.png").convert()
            level.visible_sprites.map_size = level.visible_sprites.floor_surf.get_size()
            level.visible_sprites.floor_surf = pygame.transform.scale(level.visible_sprites.floor_surf,
                                                     (level.visible_sprites.map_size[0] * self.zoom, level.visible_sprites.map_size[1] * self.zoom))
            level.visible_sprites.floor_rect = level.visible_sprites.floor_surf.get_rect(topleft=(0, 0))
            # 플레이어 재배치

            
            # 맵 변경 변수
            self.is_intro = False
            self.is_island = True
            self.is_cave = False

        screen.fill('black')
        level.run()
        screen.blit(update_fps(), (10, 0))

        # 플레이어 위치 표시
        update_position()

    def cave(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.STAGE = 'island'
                    level.current_stage = 'island'
                if event.key == pygame.K_b:
                    self.STAGE = 'cave'
                    level.current_stage = 'cave'

        if self.is_cave == False:
            # 이전 맵의 wall_block 삭제

            # 맵 재로딩
            level.create_map()
            # 맵 구성 요소
            level.visible_sprites.floor_surf = pygame.image.load("map/test_map1.png").convert()
            level.visible_sprites.map_size = level.visible_sprites.floor_surf.get_size()
            level.visible_sprites.floor_surf = pygame.transform.scale(level.visible_sprites.floor_surf,
                                                                      (level.visible_sprites.map_size[0] * self.zoom,
                                                                       level.visible_sprites.map_size[1] * self.zoom))
            level.visible_sprites.floor_rect = level.visible_sprites.floor_surf.get_rect(topleft=(0, 0))

            level.player.hitbox.x = 2000
            level.player.hitbox.y = 2200
            self.is_intro = False
            self.is_island = False
            self.is_cave = True

        screen.fill('black')
        level.run()
        screen.blit(update_fps(), (10, 0))
        # 플레이어 위치 표시
        update_position()

    def state_manager(self):
        if self.STAGE == 'intro':
            self.intro()
        if self.STAGE == 'island':
            self.island()
        if self.STAGE == 'cave':
            self.cave()

    def bgm_play(self):
        if self.is_cave and not self.cave_bgm_chan.get_busy():
            self.island_bgm_chan.stop()  # 중복 재생 방지
            self.cave_bgm_chan.play(self.cave_bgm)
        elif self.is_island and not self.island_bgm_chan.get_busy():
            self.cave_bgm_chan.stop()
            self.island_bgm_chan.play(self.island_bgm)

level = Level()
game_state = GameState()
hit_cooldown = 0
while True:
    game_state.state_manager()
    clock.tick(FPS)
    pygame.display.update()
    game_state.bgm_play()