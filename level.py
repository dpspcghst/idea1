import pygame

from bit_effect import BitEffect
from map import LEVEL1_MAP
from player import Player
from save import Save
import settings as s
from tile import Tile


class Level:

    def __init__(self):

        self.player = None
        self.world_x_shift = 0
        self.world_y_shift = 0
        self.dust_sprite = pygame.sprite.GroupSingle()

        self.surface = pygame.display.get_surface()
        self.save = Save()
        self.setup_level()
        self.current_x = 0
        # Maybe an assign method to group them all together?
        self.player_on_ground = False

    def create_jump_bit(self, position):

        if self.player.sprite.facing_right:

            position -= pygame.math.Vector2(10, 5)

        else:

            position += pygame.math.Vector2(10, -5)

        # Why not just use "self.player.sprite.rect.midbottom" for position?
        jump_bit_sprite = BitEffect(position, "jump")

        # inheritance returns an object
        self.dust_sprite.add(jump_bit_sprite)
    
    def get_player_on_ground(self):

        if self.player.sprite.on_ground:

            self.player_on_ground = True

        else:

            self.player_on_ground = False
    
    def create_landing_bit(self):

        if not (
                self.player_on_ground and self.player.sprite.on_ground
        ) and not self.dust_sprite.sprites():

            if self.player.sprite.facing_right:

                offset = pygame.math.Vector2(-10, 15)

            else:

                offset = pygame.math.Vector2()
            
            fall_dust_sprite = BitEffect(
                self.player.sprite.rect.midbottom - offset,
                "land"
            )

            # inheritance returns an object
            self.dust_sprite.add(fall_dust_sprite)

    def setup_level(self):
        
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()

        for row_index, row in enumerate(LEVEL1_MAP):

            for column_index, column in enumerate(row):

                x = column_index * s.TILE_SIZE
                y = row_index * s.TILE_SIZE

                if column == "P":

                    new_x, new_y = self.save.pull_from_save()
                                
                    if new_x and new_y:
            
                        player_sprite = Player((new_x, new_y), self.create_jump_bit)
            
                    else:
            
                        player_sprite = Player((x, y), self.create_jump_bit)
            
                    # inheritance returns an object
                    self.player.add(player_sprite)

                if column == "X":

                    tile = Tile((x, y))
                    self.tiles.add(tile)

    def scroll_x(self):

        player = self.player.sprite
        player_x = player.rect.centerx
        velocity_x = player.velocity.x

        if player_x < self.surface.get_width() * 0.25 and velocity_x < 0:

            self.world_x_shift = 1
            player.speed = 0

        elif player_x > self.surface.get_width() * 0.75 and velocity_x > 0:

            self.world_x_shift = -1
            player.speed = 0

        else:

            self.world_x_shift = 0
            player.speed = 1

    def scroll_y(self):
        """
        test branch
        """

        player = self.player.sprite
        player_y = player.rect.centery
        velocity_y = player.velocity.y

        if player_y < self.surface.get_height() * 0.25 and velocity_y < 0:

            self.world_y_shift = 1
            player.speed = 0

        elif player_y > self.surface.get_height() * 0.6 and velocity_y > 0:

            self.world_y_shift = -1
            player.speed = 0

        else:

            self.world_y_shift = 0
            player.speed = 1

    def horizontal_movement_collision(self, dt):

        player = self.player.sprite
        player.rect.x += player.velocity.x * player.speed

        for tile in self.tiles.sprites():

            if tile.rect.colliderect(player.rect):

                if player.velocity.x < 0:

                    player.rect.left = tile.rect.right
                    player.on_left = True

                    self.current_x = player.rect.left

                elif player.velocity.x > 0:

                    player.rect.right = tile.rect.left
                    player.on_right = True

                    self.current_x = player.rect.right

        if player.on_left and (
                player.rect.left < self.current_x or player.velocity.x >= 0
        ):

            player.on_left = False

        if player.on_right and (
                player.rect.right > self.current_x or player.velocity.x <= 0
        ):

            player.on_right = False

    def vertical_movement_collision(self):

        player = self.player.sprite
        player.apply_gravity()

        for tile in self.tiles.sprites():

            if tile.rect.colliderect(player.rect):

                if player.velocity.y > 0:

                    player.rect.bottom = tile.rect.top
                    player.velocity.y = 0
                    player.on_ground = True

                elif player.velocity.y < 0:

                    player.rect.top = tile.rect.bottom
                    player.velocity.y = 0
                    player.on_ceiling = True

        if (
                player.on_ground and
                player.velocity.y < 0 or player.velocity.y > 1
        ):

            player.on_ground = False

        if player.on_ceiling and player.velocity.y > 0:

            player.on_ceiling = False

    def auto_save(self):

        player = self.player.sprite
        self.save.push_to_save(player.rect.x, player.rect.y - 100)
    
    def run(self, dt):

        self.tiles.update(self.world_x_shift, self.world_y_shift)
        self.tiles.draw(self.surface)
        self.scroll_x()
        self.scroll_y()
        self.dust_sprite.update(self.world_x_shift, self.world_y_shift)
        self.dust_sprite.draw(self.surface)

        self.player.update()
        self.horizontal_movement_collision(dt)
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_bit()
        self.player.draw(self.surface)
