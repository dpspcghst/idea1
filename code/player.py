import pygame

from settings import START_POSITION
from support import import_folder


class Player(pygame.sprite.Sprite):

    def __init__(self, position, create_jump_particles):

        super().__init__()
        # self.import_character_assets()
        # # self.frame_index = 0
        # self.animation_speed = 0.15
        # self.image = self.animations["idle"][self.frame_index]
        self.image = pygame.Surface((64, 64))
        self.image.fill("black")
        self.rect = self.image.get_rect(topleft=position)
        print(self.rect.x)

        self.dust_run_particles = []
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.surface = pygame.display.get_surface()
        self.create_jump_particles = create_jump_particles

        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 1)
        self.speed = 100
        self.gravity = 1
        self.jump_speed = -8
        self.terminal_velocity = 20
        
        self.status = "idle"
        self.facing_right = True
        self.on_ceiling = False
        self.on_ground = False
        self.on_left = False
        self.on_right = False

        self.is_dead = False

        self.going_right = ""

    # def import_character_assets(self):
    #
    #     character_path = "../graphics/character/"
    #     self.animations = {
    #         "fall": [], "idle": [], "jump": [], "run": []
    #     }
    #
    #     for animation in self.animations.keys():
    #
    #         full_path = character_path + animation
    #         self.animations[animation] = import_folder(full_path)
    
    def import_dust_run_particles(self):

        run_path = "../graphics/character/dust_particles/run"
        self.dust_run_particles = import_folder(run_path)
    
    # def animate(self):
    #
    #     animation = self.animations[self.status]
    #     self.frame_index += self.animation_speed
    #
    #     if self.frame_index >= len(animation):
    #
    #         self.frame_index = 0
    #
    #     image = animation[int(self.frame_index)]
    #
    #     if self.facing_right:
    #
    #         self.image = image
    #
    #     else:
    #
    #         flipped_image = pygame.transform.flip(image, True, False)
    #         self.image = flipped_image
    #
    #     if self.on_ground and self.on_right:
    #
    #         self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
    #
    #     elif self.on_ground and self.on_left:
    #
    #         self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
    #
    #     elif self.on_ground:
    #
    #         self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
    #
    #     elif self.on_ceiling and self.on_right:
    #
    #         self.rect = self.image.get_rect(topright=self.rect.topright)
    #
    #     elif self.on_ceiling and self.on_left:
    #
    #         self.rect = self.image.get_rect(topleft=self.rect.topleft)
    #
    #     elif self.on_ceiling:
    #
    #         self.rect = self.image.get_rect(midtop=self.rect.midtop)
    #
    #     else:
    #
    #         self.rect = self.image.get_rect(center=self.rect.center)

    def run_dust_animation(self):

        if self.status == "run" and self.on_ground:

            self.dust_frame_index += self.dust_animation_speed

            if self.dust_frame_index >= len(self.dust_run_particles):

                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:

                position = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.surface.blit(dust_particle, position)

            else:

                position = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(
                    dust_particle, True, False
                )
                self.surface.blit(flipped_dust_particle, position)
    
    def get_input(self):
        """
        delta time
        """

        keys = pygame.key.get_pressed()
        jump_released = True

        if not self.is_dead:
        
            if keys[pygame.K_LEFT]:
    
                self.velocity.x = -1
                self.facing_right = False
                self.going_right = False
    
            elif keys[pygame.K_RIGHT]:
    
                self.velocity.x = 1
                self.facing_right = True
                self.going_right = True
    
            else:
    
                self.velocity.x = 0
                self.going_right = ""
    
            if keys[pygame.K_SPACE] and self.on_ground:
    
                self.jump()
                self.create_jump_particles(self.rect.midbottom)
                jump_released = False

        else:

            self.velocity.x = 0
            self.velocity.y = 0

    def get_status(self):

        if self.velocity.y > 1:

            self.status = "fall"

        elif self.velocity.y < 0:

            self.status = "jump"

        else:

            if self.velocity.x == 0:

                self.status = "idle"

            else:
                
                self.status = "run"

    def apply_gravity(self):

        self.velocity.y += self.acceleration.y
        self.velocity.y = min(self.velocity.y, self.terminal_velocity)
        self.rect.y += self.velocity.y

    def jump(self):

        self.velocity.y = self.jump_speed

    def update(self):

        self.get_input()
        self.get_status()
        # self.animate()
        self.run_dust_animation()
