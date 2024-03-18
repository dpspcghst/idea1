import core as c
from timer import Timer


class Tooth(c.Sprite):

    def __init__(self, collision_sprites, frames, groups, position):

        super().__init__(groups)

        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft=position)
        self.old_rect = self.rect.copy()
        self.z = c.Z_LAYERS["main"]

        self.direction = c.choice((-1, 1))
        self.collision_rectangles = [sprite.rect for sprite in collision_sprites]
        self.speed = 200

        self.hit_timer = Timer(250)

    def reverse(self):

        if not self.hit_timer.active:
            
            self.direction *= -1
            self.hit_timer.activate()
    
    def update(self, delta_time):

        self.hit_timer.update()
        
        # animate
        self.frame_index += c.ANIMATION_SPEED * delta_time
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        
        if self.direction < 0:
            
            self.image = c.flip(self.image, True, False)
            
        else:
            
            pass

        # move
        self.rect.x += self.direction * self.speed * delta_time

        # reverse direction
        floor_rectangle_left = c.FRect(self.rect.bottomleft, (1, 1))
        floor_rectangle_right = c.FRect(self.rect.bottomright, (-1, 1))
        wall_rectangle = c.FRect(self.rect.topleft + c.Vector2(-1, 0), (self.rect.width + 2, 1))

        if (
            floor_rectangle_right.collidelist(self.collision_rectangles) < 0 < self.direction or
            floor_rectangle_left.collidelist(self.collision_rectangles) < 0 and
            self.direction < 0 or
            wall_rectangle.collidelist(self.collision_rectangles) != -1
        ):

            self.reverse()


class Shell(c.Sprite):

    def __init__(self, create_pearl, frames, groups, player, position, reverse):

        super().__init__(groups)

        if reverse:
            
            self.frames = {}

            for key, surfaces in frames.items():

                self.frames[key] = [c.flip(surface, True, False) for surface in surfaces]

            self.bullet_direction = -1

        else:

            self.frames = frames
            self.bullet_direction = 1

        self.frame_index = 0
        self.state = "idle"
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft=position)
        self.old_rect = self.rect.copy()
        self.z = c.Z_LAYERS["main"]
        self.player = player
        self.shoot_timer = Timer(3000)
        self.has_fired = False
        self.create_pearl = create_pearl

    def state_management(self):

        player_position = c.Vector2(self.player.hit_box_rectangle.center)
        shell_position = c.Vector2(self.rect.center)
        player_near = shell_position.distance_to(player_position) < 500

        if self.bullet_direction > 0:
            
            player_front = shell_position.x < player_position.x

        else:

            player_front = shell_position.x > player_position.x

        player_level = abs(shell_position.y - player_position.y) < 30

        if player_near and player_front and player_level and not self.shoot_timer.active:

            self.state = "fire"
            self.frame_index = 0
            self.shoot_timer.activate()

    def update(self, delta_time):

        self.shoot_timer.update()
        self.state_management()

        # animation / attack
        self.frame_index += c.ANIMATION_SPEED * delta_time

        if self.frame_index < len(self.frames[self.state]):

            self.image = self.frames[self.state][int(self.frame_index)]

            # fire
            if self.state == "fire" and int(self.frame_index) == 3 and not self.has_fired:

                self.create_pearl(self.bullet_direction, self.rect.center)
                self.has_fired = True

        else:

            self.frame_index = 0

            if self.state == "fire":

                self.state = "idle"
                self.has_fired = False


class Pearl(c.Sprite):

    def __init__(self, direction, groups, position, speed, surface):

        self.pearl = True
        
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_frect(center=position + c.Vector2(50 * direction, 0))
        self.direction = direction
        self.speed = speed
        self.z = c.Z_LAYERS["main"]
        self.timers = {
            "lifetime": Timer(5000),
            "reverse": Timer(250)
        }
        self.timers["lifetime"].activate()

    def reverse(self):

        if not self.timers["reverse"].active:

            self.direction *= -1
            self.timers["reverse"].activate()
    
    def update(self, delta_time):

        for timer in self.timers.values():

            timer.update()

        self.rect.x += self.direction * self.speed * delta_time

        if not self.timers["lifetime"].active:

            self.kill()
