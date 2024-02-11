import pygame

from support import import_folder


class BitEffect(pygame.sprite.Sprite):

    def __init__(self, position: tuple, bit_type: str):

        super().__init__()  # inheritance returns an object
        self.frame_index = 0
        self.animation_speed = 0.5

        if bit_type == "jump":

            jump_path = "../graphics/character/dust_particles/jump"
            self.frames = import_folder(jump_path)

        if bit_type == "land":

            land_path = "../graphics/character/dust_particles/land"
            self.frames = import_folder(land_path)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=position)

    def animate(self):

        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):

            self.kill()

        else:

            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift: int, y_shift: int):

        self.animate()
        self.rect.x += x_shift
        self.rect.y += y_shift
