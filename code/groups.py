import core as c
from sprites import CloudSprite, CustomSprite
from timer import Timer


class WorldSprites(c.Group):

    def __init__(self, data):

        super().__init__()
        self.surface = c.get_surface()
        self.data = data
        self.offset = c.Vector2()

    def draw(self, target_position):

        self.offset.x = -(target_position[0] - c.WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - c.WINDOW_HEIGHT / 2)

        # background
        for sprite in sorted(self, key = lambda sprite: sprite.z):

            if sprite.z < c.Z_LAYERS["main"]:
            
                if sprite.z == c.Z_LAYERS["path"]:
    
                    if sprite.level <= self.data.unlocked_level:
    
                        self.surface.blit(sprite.image, sprite.rect.topleft + self.offset)
    
                else:
                    
                    self.surface.blit(sprite.image, sprite.rect.topleft + self.offset)

        # main
        for sprite in sorted(self, key = lambda sprite: sprite.rect.center):

            if sprite.z == c.Z_LAYERS["main"]:

                if hasattr(sprite, "icon"):

                    self.surface.blit(sprite.image, sprite.rect.topleft + self.offset + c.Vector2(0, -28))
                
                else:
                    
                    self.surface.blit(sprite.image, sprite.rect.topleft + self.offset)

class AllSprites(c.Group):

    def __init__(self, clouds, height, horizon_line, width, bg_tile=None, top_limit=0):

        super().__init__()

        self.surface = c.get_surface()
        self.offset = c.Vector2()
        self.width = width * c.TILE_SIZE
        self.height = height * c.TILE_SIZE
        self.borders = {
            "bottom": -self.height + c.WINDOW_HEIGHT,
            "left": 0,
            "right": -self.width + c.WINDOW_WIDTH,
            "top": top_limit
        }
        self.sky = not bg_tile
        self.horizon_line = horizon_line

        if bg_tile:

            for column in range(width):

                for row in range(-int(top_limit / c.TILE_SIZE) - 1, height):

                    x = column * c.TILE_SIZE
                    y = row * c.TILE_SIZE

                    CustomSprite((x, y), self, bg_tile, -1)

        else:  # sky

            self.large_cloud = clouds["large"]
            self.small_clouds = clouds["small"]
            self.cloud_direction = -1

            # large cloud
            self.large_cloud_speed = 50
            self.large_cloud_x = 0
            self.large_cloud_tiles = int(self.width / self.large_cloud.get_width()) + 2
            self.large_cloud_height = self.large_cloud.get_height()
            self.large_cloud_width = self.large_cloud.get_width()

            # small cloud
            self.cloud_timer = Timer(2500, self.create_cloud, True)
            self.cloud_timer.activate()
            for cloud in range(20):

                position = (c.randint(0, self.width), c.randint(self.borders["top"], self.horizon_line))
                surface = c.choice(self.small_clouds)
                CloudSprite(self, position, surface)

    def camera_constraint(self):

        if self.offset.x < self.borders["left"]:

            self.offset.x = self.offset.x

        else:

            self.offset.x = self.borders["left"]

        if self.offset.x > self.borders["right"]:

            self.offset.x = self.offset.x

        else:

            self.offset.x = self.borders["right"]

        if self.offset.y > self.borders["bottom"]:

            self.offset.y = self.offset.y

        else:

            self.offset.y = self.borders["bottom"]

        if self.offset.y < self.borders["top"]:

            self.offset.y = self.offset.y

        else:

            self.offset.y = self.borders["top"]
    
    def draw_sky(self):

        self.surface.fill("#ddc6a1")
        # self.surface.fill(c.tense_yellow)
        horizon_position = self.horizon_line + self.offset.y

        sea_rectangle = c.FRect(0, horizon_position, c.WINDOW_WIDTH, c.WINDOW_HEIGHT - horizon_position)
        c.rect(self.surface, "#92a9ce", sea_rectangle)

        # horizon lines
        c.line(self.surface, "#f5f1de", (0, horizon_position), (c.WINDOW_WIDTH, horizon_position), 4)
    
    def draw_large_cloud(self, delta_time):
    
        self.large_cloud_x += self.cloud_direction * self.large_cloud_speed * delta_time

        if self.large_cloud_x <= -self.large_cloud_width:

            self.large_cloud_x = 0
        
        for cloud in range(self.large_cloud_tiles):

            left = self.large_cloud_x + self.large_cloud_width * cloud + self.offset.x
            top = self.horizon_line - self.large_cloud_height + self.offset.y
            self.surface.blit(self.large_cloud, (left, top))
    
    def create_cloud(self):

        position = (
            c.randint(self.width + 500, self.width + 600),
            c.randint(self.borders["top"], self.horizon_line)
        )
        surface = c.choice(self.small_clouds)
        CloudSprite(self, position, surface)
    
    def draw(self, delta_time, target_position):

        self.offset.x = -(target_position[0] - c.WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - c.WINDOW_HEIGHT / 2)
        self.camera_constraint()

        if self.sky:

            self.cloud_timer.update()
            self.draw_sky()
            self.draw_large_cloud(delta_time)
        
        for sprite in sorted(self, key=lambda entity: entity.z):

            offset_position = sprite.rect.topleft + self.offset
            self.surface.blit(sprite.image, offset_position)
