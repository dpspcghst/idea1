import pygame

class Collectible(pygame.sprite.Sprite):

    def __init__(self, size):

        super().__init__()

        self.image = pygame.Surface((size, size))
        self.image.fill("white")
        self.position = (64, 352)
        self.rect = self.image.get_rect(topleft = self.position)

    def update(self, x_shift, y_shift):

        self.rect.x += x_shift
        self.rect.y += y_shift
