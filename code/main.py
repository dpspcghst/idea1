from sys import exit

import pygame
from pygame.locals import QUIT

from debug import debug
from level import Level
import settings as s
from ui import UI


class Game:

    def __init__(self):

        pygame.init()
        pygame.display.set_caption(s.TITLE)
        self.icon_image = pygame.image.load("../graphics/ensōurobo_icon.png")
        pygame.display.set_icon(self.icon_image)
        self.surface = pygame.display.set_mode(size=(s.WIDTH, s.HEIGHT))
        self.ui = UI()
        self.background = pygame.image.load("../graphics/background.png")
        self.scaled_image = pygame.transform.scale(
            self.background, (s.WIDTH, s.HEIGHT)
        )
        self.level = Level()
        self.clock = pygame.time.Clock()

    def run(self):
    
        # self.ui.run_splash()

        dt = 0

        while s.RUNNING:
        
            for event in pygame.event.get():
        
                if event.type == QUIT:
        
                    s.RUNNING = False
                    pygame.quit()
                    exit()

            self.surface.blit(self.scaled_image, (0, 0))
            # debug(dt)
            self.level.run(dt)
            pygame.display.update()
            dt = self.clock.tick(s.FPS) / 1000


if __name__ == "__main__":
    game = Game()
    game.run()
