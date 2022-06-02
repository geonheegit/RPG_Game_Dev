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
        self.is_test_stage = False
        self.zoom = 2
        self.STAGE = 'intro'

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
                    self.STAGE = 'test_stage'
                    level.current_stage = 'test_stage'

        if self.is_intro == False:
            level.player.hitbox.x = 0
            level.player.hitbox.y = 0
            self.is_intro = True
            self.is_island = False
            self.is_test_stage = False

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
                    self.STAGE = 'test_stage'
                    level.current_stage = 'test_stage'

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
            level.player.hitbox.x = 2000
            level.player.hitbox.y = 2200
            level.enemy.hitbox.x = 2000
            level.enemy.hitbox.y = 2000
            
            # 맵 변경 변수
            self.is_intro = False
            self.is_island = True
            self.is_test_stage = False

        screen.fill('black')
        level.run()
        screen.blit(update_fps(), (10, 0))

        # 플레이어 위치 표시
        update_position()

    def test_stage(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.STAGE = 'island'
                    level.current_stage = 'island'
                if event.key == pygame.K_b:
                    self.STAGE = 'test_stage'
                    level.current_stage = 'test_stage'

        if self.is_test_stage == False:
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
            self.is_test_stage = True

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
        if self.STAGE == 'test_stage':
            self.test_stage()

level = Level()
game_state = GameState()

while True:
    game_state.state_manager()
    clock.tick(FPS)
    pygame.display.update()