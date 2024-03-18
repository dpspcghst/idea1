import core as c


class CustomSprite(c.Sprite):

    def __init__(
        self, position, groups=None, surface=c.Surface((c.TILE_SIZE, c.TILE_SIZE)), z=c.Z_LAYERS["main"]
    ):

        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.old_rect = self.rect.copy()
        self.z = z


class AnimatedSprite(CustomSprite):

    def __init__(self, frames, groups, position, animation_speed=c.ANIMATION_SPEED, z=c.Z_LAYERS["main"]):

        self.frames = frames
        self.frame_index = 0
        
        super().__init__(position, groups, self.frames[self.frame_index], z)

        self.animation_speed = animation_speed

    def animate(self, delta_time):

        self.frame_index += self.animation_speed * delta_time
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, delta_time):

        self.animate(delta_time)


class ItemSprite(AnimatedSprite):

    def __init__(self, data, frames, groups, item_type, position):

        super().__init__(frames, groups, position)

        self.rect.center = position
        self.item_type = item_type
        self.data = data

    def activate(self):

        if self.item_type == "diamond":

            self.data.coins += 20
            
        if self.item_type == "gold":

            self.data.coins += 5

        if self.item_type == "potion":

            self.data.health += 1
        
        if self.item_type == "skull":

            self.data.coins += 50
        
        if self.item_type == "silver":

            self.data.coins += 1


class ParticleEffectSprite(AnimatedSprite):

    def __init__(self, frames, groups, position):

        super().__init__(frames, groups, position)
        self.rect.center = position
        self.z = c.Z_LAYERS["fg"]

    def animate(self, delta_time):

        self.frame_index += self.animation_speed * delta_time

        if self.frame_index < len(self.frames):

            self.image = self.frames[int(self.frame_index)]

        else:

            self.kill()


class MovingSprite(AnimatedSprite):

    def __init__(self, frames, groups, move_direction, start_position, end_position, speed, flip_image=False):
        
        super().__init__(frames, groups, start_position)

        if move_direction == "x":

            self.rect.midleft = start_position

        else:

            self.rect.midtop = start_position
        
        self.start_position = start_position
        self.end_position = end_position

        # movement
        self.moving = True
        self.speed = speed
        self.direction = c.Vector2(1, 0) if move_direction == "x" else c.Vector2(0, 1)
        self.move_direction = move_direction

        self.flip_image = flip_image
        self.reverse = {"x": False, "y": False}

    def check_border(self):

        if self.move_direction == "x":

            if self.rect.right >= self.end_position[0] and self.direction.x == 1:
                
                self.direction.x = -1
                self.rect.right = self.end_position[0]
                # print("something else")

            if self.rect.left <= self.start_position[0] and self.direction.x == -1:

                self.direction.x = 1
                self.rect.left = self.start_position[0]
                # print("something")

            self.reverse["x"] = True if self.direction.x < 0 else False

        else:

            if self.rect.bottom >= self.end_position[1] and self.direction.y == 1:

                self.direction.y = -1
                self.rect.bottom = self.end_position[1]

            if self.rect.top <= self.start_position[1] and self.direction.y == -1:

                self.direction.y = 1
                self.rect.top = self.start_position[1]

            self.reverse["y"] = True if self.direction.y > 0 else False
    
    def update(self, delta_time):

        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * delta_time
        self.check_border()

        self.animate(delta_time)

        if self.flip_image:

            self.image = c.flip(self.image, self.reverse["x"], self.reverse["y"])


class SpikedSprite(CustomSprite):

    def __init__(self, start_angle, end_angle, groups, position, radius, speed, surface, z=c.Z_LAYERS["main"]):

        self.center = position
        self.radius = radius
        self.speed = speed
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.angle = self.start_angle
        self.direction = 1
        self.full_circle = True if self.end_angle == -1 else False

        # trigonometry
        x = self.center[0] + c.cos(c.radians(self.angle)) * self.radius
        y = self.center[1] + c.sin(c.radians(self.angle)) * self.radius

        super().__init__((x, y), groups, surface, z)

    def update(self, delta_time):

        self.angle += self.direction * self.speed * delta_time

        if not self.full_circle:

            if self.angle >= self.end_angle:

                self.direction = -1

            if self.angle < self.start_angle:

                self.direction = 1

        x = self.center[0] + c.cos(c.radians(self.angle)) * self.radius
        y = self.center[1] + c.sin(c.radians(self.angle)) * self.radius

        self.rect.center = (x, y)

class CloudSprite(CustomSprite):

    def __init__(self, groups, position, surface, z=c.Z_LAYERS["clouds"]):

        super().__init__(position, groups, surface, z)

        self.speed = c.randint(50, 120)
        self.direction = -1
        self.rect.midbottom = position

    def update(self, delta_time):

        self.rect.x += self.direction * self.speed * delta_time

        if self.rect.right <= 0:

            self.kill()

class NodeSprite(c.Sprite):

    def __init__(self, data, groups, level, paths, position, surface):

        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center=(position[0] + c.TILE_SIZE / 2, position[1] + c.TILE_SIZE / 2))
        self.z = c.Z_LAYERS["path"]
        self.level = level
        self.data = data
        self.paths = paths
        self.grid_position = (int(position[0] / c.TILE_SIZE), int(position[1] / c.TILE_SIZE))

    def can_move(self, direction):

        if direction in list(self.paths.keys()) and int(self.paths[direction][0][0]) <= self.data.unlocked_level:

            return True

class IconSprite(c.Sprite):

    def __init__(self, frames, groups, position):

        super().__init__(groups)
        self.icon = True
        self.path = None
        self.direction = c.Vector2()
        self.speed = 400

        # image
        self.frames = frames
        self.frame_index = 0
        self.state = "idle"
        self.image = self.frames[self.state][self.frame_index]
        self.z = c.Z_LAYERS["main"]

        # rect
        self.rect = self.image.get_frect(center=position)

    def start_move(self, path):

        self.rect.center = path[0]
        self.path = path[1:]
        self.find_path()

    def find_path(self):

        if self.path:

            if self.rect.centerx == self.path[0][0]:  # vertical

                self.direction = c.Vector2(0, 1 if self.path[0][1] > self.rect.centery else - 1)

            else:  # horizontal

                self.direction = c.Vector2(1 if self.path[0][0] > self.rect.centerx else - 1, 0)

        else:

            self.direction = c.Vector2()

    def point_collision(self):

        # down & up
        if (
            self.direction.y == 1 and self.rect.centery >= self.path[0][1] or
            self.direction.y == -1 and self.rect.centery <= self.path[0][1]
        ):

            self.rect.centery = self.path[0][1]
            del self.path[0]
            self.find_path()

        # left & right
        if (
            self.direction.x == 1 and self.rect.centerx >= self.path[0][0] or
            self.direction.x == -1 and self.rect.centerx <= self.path[0][0]
        ):

            self.rect.centerx = self.path[0][0]
            del self.path[0]
            self.find_path()
    
    def animate(self, delta_time):

        self.frame_index += c.ANIMATION_SPEED * delta_time
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]

    def get_state(self):

        self.state = "idle"

        if self.direction == c.Vector2(0,1): self.state = "down"

        if self.direction == c.Vector2(-1,0): self.state = "left"
        
        if self.direction == c.Vector2(1,0): self.state = "right"
        
        if self.direction == c.Vector2(0,-1): self.state = "up"

    def update(self, delta_time):

        if self.path:

            self.point_collision()
            self.rect.center += self.direction * self.speed * delta_time

        self.get_state()
        self.animate(delta_time)

class PathSprite(CustomSprite):
    
    def __init__(self, groups, level, position, surface):

        super().__init__(position, groups, surface, c.Z_LAYERS["path"])

        self.level = level
