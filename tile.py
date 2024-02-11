import pygame

import settings as s

class Tile(pygame.sprite.Sprite):

    def __init__(self, position, id=0):

        super().__init__()
        self.image = pygame.Surface((s.TILE_SIZE, s.TILE_SIZE))        
        self.image.fill(s.L_GRAY)        
        self.rect = self.image.get_rect(topleft=position)
        self.id = id

    def draw_line(self):

        if self.id == 0:

            pass

        elif self.id == 1:

            pygame.draw.aaline(self.image, "black", (start), (end))
    
    def update(self, x_shift, y_shift):

        self.rect.x += x_shift
        self.rect.y += y_shift
        self.draw_line()
