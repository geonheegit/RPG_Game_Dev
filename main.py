import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):

        # 기본 설정
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Adventure & Puzzle')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial",18)

        self.level = Level()

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps,1,pygame.Color("white"))
        return fps_text

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            self.screen.blit(self.update_fps(), (10, 0))
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()