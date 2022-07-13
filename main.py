import pygame, sys
import settings
from level import Level
from csv_read import *
import tile

pygame.init()
pygame.display.set_caption('Adventure & Puzzle')
clock = pygame.time.Clock()
font = pygame.font.Font("font/Infinite Darkness.ttf",22)
kr_font = pygame.font.Font("font/OK CHAN.ttf", 22)
main_screen_kr_font = pygame.font.Font("font/OK CHAN.ttf", 30)

WIDTH = settings.WIDTH
HEIGTH = settings.HEIGTH
FPS = settings.FPS

screen = pygame.display.set_mode((WIDTH, HEIGTH))

minimap_island = pygame.image.load("map/minimap_island.png").convert_alpha()
minimap_cave = pygame.image.load("map/minimap_cave.png").convert_alpha()
minimap_on = False
minimap_posx = 784

question_mark_icon = pygame.image.load("graphics/icon/question_mark.png").convert_alpha()

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

def question_mark():
    screen.blit(question_mark_icon, (10, 100))
    if 10 <= pygame.mouse.get_pos()[0] <= 60 and 100 <= pygame.mouse.get_pos()[1] <= 150:
        if game_state.STAGE == 'cave':
            screen.blit(kr_font.render("m키를 눌러서 미니맵을 켜고 끌 수 있습니다.", 1,
                                        pygame.Color("white")), (WIDTH / 4 + 70, 100))
        else:
            screen.blit(kr_font.render("m키를 눌러서 미니맵을 켜고 끌 수 있습니다.", 1,
                                       pygame.Color("black")), (WIDTH / 4 + 70, 100))

class GameState():
    def __init__(self):
        self.is_intro = True
        self.is_island = False
        self.is_cave = False
        self.is_beach = False
        self.is_forest = False
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
                if event.key == pygame.K_RETURN:
                    self.STAGE = 'island'
                    level.current_stage = 'island'

        # 처음 시작했을 때 화면 설정
        if self.is_intro == False:
            level.player.hitbox.x = 0
            level.player.hitbox.y = 0
            self.is_intro = True
            self.is_island = False
            self.is_cave = False
            self.is_beach = False
            self.is_forest = False

        screen.blit(main_screen_kr_font.render("게임을 시작하려면 엔터를 누르세요.", 0,
                                pygame.Color("white")), (WIDTH / 4 + 70, HEIGTH / 2))

    def island(self):
        global minimap_on
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                # 미니맵 토글
                if event.key == pygame.K_m:
                    if not minimap_on:
                        minimap_on = True
                    else:
                        minimap_on = False
                # 맵 이동 트리거
                if event.key == pygame.K_SPACE:
                    # 동굴 x 1900 - 2000, y 2300 - 2400 / 숲 x 2400 - 2500, y 600 - 700 / 해변 x 600 - 800, y 2800 - 2900
                    if 1900 < level.player.hitbox.x < 2000 and 2300 < level.player.hitbox.y < 2400:
                        self.STAGE = 'cave'
                        level.current_stage = 'cave'

                    if 600 < level.player.hitbox.x < 800 and 2800 < level.player.hitbox.y < 2900:
                        self.STAGE = 'beach'
                        level.current_stage = 'beach'
                        
                    if 2400 < level.player.hitbox.x < 2500 and 600 < level.player.hitbox.y < 700:  # 숲 트리거
                        self.STAGE = 'forest'
                        level.current_stage = 'forest'


        if self.is_island == False:
            # 맵 재로딩
            level.create_map()  # 타일 초기화
            # 맵 구성 요소
            level.visible_sprites.floor_surf = pygame.image.load("map/island.png").convert()
            level.visible_sprites.map_size = level.visible_sprites.floor_surf.get_size()
            level.visible_sprites.floor_surf = pygame.transform.scale(level.visible_sprites.floor_surf,
                                                     (level.visible_sprites.map_size[0] * self.zoom, level.visible_sprites.map_size[1] * self.zoom))
            level.visible_sprites.floor_rect = level.visible_sprites.floor_surf.get_rect(topleft=(0, 0))
            # 플레이어 재배치
            level.player.hitbox.x = 1500
            level.player.hitbox.y = 2000
            
            # 맵 변경 변수
            self.is_intro = False
            self.is_island = True
            self.is_cave = False
            self.is_beach = False
            self.is_forest = False

        screen.fill('black')
        level.run()
        screen.blit(update_fps(), (10, 0))
        question_mark()

        if minimap_on:
            if self.STAGE == 'island' and level.current_stage == 'island':
                screen.blit(minimap_island, (minimap_posx, 0))

        # 플레이어 위치 표시
        update_position()

    def cave(self):
        global minimap_on
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # 미니맵 토글
                if event.key == pygame.K_m:
                    if not minimap_on:
                        minimap_on = True
                    else:
                        minimap_on = False
                if event.key == pygame.K_SPACE:
                    # 동굴 x 1900 - 2000, y 2300 - 2400 / 숲 x 2400 - 2500, y 600 - 700 / 해변 x 600 - 800, y 2800 - 2900
                    if 800 < level.player.hitbox.x < 900 and 3100 < level.player.hitbox.y < 3200:
                        self.STAGE = 'island'
                        level.current_stage = 'island'

        if self.is_cave == False:
            # 맵 재로딩 (이전 맵의 wall_block 삭제)
            level.create_map()
            # 맵 구성 요소
            level.visible_sprites.floor_surf = pygame.image.load("map/cave.png").convert()
            level.visible_sprites.map_size = level.visible_sprites.floor_surf.get_size()
            level.visible_sprites.floor_surf = pygame.transform.scale(level.visible_sprites.floor_surf,
                                                                      (level.visible_sprites.map_size[0] * self.zoom,
                                                                       level.visible_sprites.map_size[1] * self.zoom))
            level.visible_sprites.floor_rect = level.visible_sprites.floor_surf.get_rect(topleft=(0, 0))

            level.player.hitbox.x = 100
            level.player.hitbox.y = 60
            self.is_intro = False
            self.is_island = False
            self.is_cave = True
            self.is_beach = False
            self.is_forest = False

        screen.fill('black')
        level.run()
        screen.blit(update_fps(), (10, 0))
        question_mark()

        if minimap_on:
            if self.STAGE == 'cave' and level.current_stage == 'cave':
                screen.blit(minimap_cave, (minimap_posx, 0))

        # 플레이어 위치 표시
        update_position()

    def beach(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 동굴 x 1900 - 2000, y 2300 - 2400 / 숲 x 2400 - 2500, y 600 - 700 / 해변 x 600 - 800, y 2800 - 2900
                    if 600 < level.player.hitbox.x < 800 and 1100 < level.player.hitbox.y < 1200:
                        self.STAGE = 'island'
                        level.current_stage = 'island'

        if self.is_beach == False:
            # 맵 재로딩
            level.create_map()  # 타일 초기화
            # 맵 구성 요소
            level.visible_sprites.floor_surf = pygame.image.load("map/beach.png").convert()
            level.visible_sprites.map_size = level.visible_sprites.floor_surf.get_size()
            level.visible_sprites.floor_surf = pygame.transform.scale(level.visible_sprites.floor_surf,
                                                                      (level.visible_sprites.map_size[0] * self.zoom,
                                                                       level.visible_sprites.map_size[1] * self.zoom))
            level.visible_sprites.floor_rect = level.visible_sprites.floor_surf.get_rect(topleft=(0, 0))
            # 플레이어 재배치
            level.player.hitbox.x = 120
            level.player.hitbox.y = 1100

            # 맵 변경 변수
            self.is_intro = False
            self.is_island = False
            self.is_cave = False
            self.is_beach = True
            self.is_forest = False

        screen.fill('black')
        level.run()
        screen.blit(update_fps(), (10, 0))
        question_mark()

        # 플레이어 위치 표시
        update_position()

    def forest(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 동굴 x 1900 - 2000, y 2300 - 2400 / 숲 x 2400 - 2500, y 600 - 700 / 해변 x 600 - 800, y 2800 - 2900
                    if 1700 < level.player.hitbox.x < 1800 and 200 < level.player.hitbox.y < 300:  # 숲에서 무인도로 (수정 필요)
                        self.STAGE = 'island'
                        level.current_stage = 'island'

        if self.is_forest == False:
            # 맵 재로딩
            level.create_map()  # 타일 초기화
            # 맵 구성 요소
            level.visible_sprites.floor_surf = pygame.image.load("map/forest.png").convert()  # forest 이미지
            level.visible_sprites.map_size = level.visible_sprites.floor_surf.get_size()
            level.visible_sprites.floor_surf = pygame.transform.scale(level.visible_sprites.floor_surf,
                                                                      (level.visible_sprites.map_size[0] * self.zoom,
                                                                       level.visible_sprites.map_size[1] * self.zoom))
            level.visible_sprites.floor_rect = level.visible_sprites.floor_surf.get_rect(topleft=(0, 0))
            # 플레이어 재배치
            level.player.hitbox.x = 30
            level.player.hitbox.y = 300

            # 맵 변경 변수
            self.is_intro = False
            self.is_island = False
            self.is_cave = False
            self.is_beach = False
            self.is_forest = True

        screen.fill('black')
        level.run()
        screen.blit(update_fps(), (10, 0))
        question_mark()

        # 플레이어 위치 표시
        update_position()

    def state_manager(self):
        if self.STAGE == 'intro':
            self.intro()
        if self.STAGE == 'island':
            self.island()
        if self.STAGE == 'cave':
            self.cave()
        if self.STAGE == 'beach':
            self.beach()
        if self.STAGE == 'forest':
            self.forest()

    def text_renderer(self):
        # island에서 각스테이지 진입 도움말 텍스트
        if self.STAGE == 'island' and level.current_stage == 'island':
            if 1900 < level.player.hitbox.x < 2000 and 2300 < level.player.hitbox.y < 2400:
                screen.blit(kr_font.render("동굴에 진입하려면 스페이스바를 누르세요.", 1,
                                    pygame.Color("black")), (WIDTH / 4 + 70, 100))

            if 600 < level.player.hitbox.x < 800 and 2800 < level.player.hitbox.y < 2900:
                screen.blit(kr_font.render("해변에 진입하려면 스페이스바를 누르세요.", 1,
                                           pygame.Color("black")), (WIDTH / 4 + 70, 100))

            if 2400 < level.player.hitbox.x < 2500 and 600 < level.player.hitbox.y < 700:
                screen.blit(kr_font.render("숲에 진입하려면 스페이스바를 누르세요.", 1,
                                           pygame.Color("black")), (WIDTH / 4 + 70, 100))

        # cave에서 island로 이동 도움말 텍스트
        if self.STAGE == 'cave' and level.current_stage == 'cave':
            if 800 < level.player.hitbox.x < 900 and 3100 < level.player.hitbox.y < 3200:
                screen.blit(kr_font.render("무인도로 다시 돌아가려면 스페이스바를 누르세요.", 1,
                                           pygame.Color("black")), (WIDTH / 4 + 70, 100))

        # beach에서 island로 이동 도움말 텍스트
        if self.STAGE == 'beach' and level.current_stage == 'beach':
            if 600 < level.player.hitbox.x < 800 and 1100 < level.player.hitbox.y < 1200:
                screen.blit(kr_font.render("무인도로 다시 돌아가려면 스페이스바를 누르세요.", 1,
                                           pygame.Color("black")), (WIDTH / 4 + 70, 100))

        # forest에서 island로 이동 도움말 텍스트
        if self.STAGE == 'forest' and level.current_stage == 'forest':
            if 1700 < level.player.hitbox.x < 1800 and 200 < level.player.hitbox.y < 300:
                screen.blit(kr_font.render("무인도로 다시 돌아가려면 스페이스바를 누르세요.", 1,
                                           pygame.Color("black")), (WIDTH / 4 + 70, 100))

    def bgm_play(self):
        if self.is_cave and not self.cave_bgm_chan.get_busy():
            self.island_bgm_chan.stop()  # 중복 재생 방지
            self.cave_bgm_chan.play(self.cave_bgm)
        elif self.is_island and not self.island_bgm_chan.get_busy():
            self.cave_bgm_chan.stop()
            self.island_bgm_chan.play(self.island_bgm)

level = Level()
game_state = GameState()

while True:
    game_state.state_manager()
    game_state.text_renderer()

    clock.tick(FPS)
    pygame.display.update()
    game_state.bgm_play()