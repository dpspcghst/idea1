import core as c
from enemies import Pearl, Shell, Tooth
from groups import AllSprites
from player import Player
import sprites as s


class Level:

    def __init__(self, data, level_frames, tmx_map):

        self.surface = c.get_surface()
        self.data = data

        # level data
        self.level_right = tmx_map.width * c.TILE_SIZE
        self.level_bottom = tmx_map.height * c.TILE_SIZE
        
        tmx_level_properties = tmx_map.get_layer_by_name("Data")[0].properties

        if tmx_level_properties["bg"]:

            bg_tile = level_frames["bg_tile"][tmx_level_properties["bg"]]

        else:

            bg_tile = None

        #  groups
        self.all_sprites = AllSprites(
            clouds= {
                "large": level_frames["big_cloud"],
                "small": level_frames["small_cloud"]
            },
            height=tmx_map.height,
            horizon_line=tmx_level_properties["horizon_line"],
            width=tmx_map.width,
            bg_tile=bg_tile,
            top_limit=tmx_level_properties["top_limit"]
        )
        self.collision_sprites = c.Group()
        self.damage_sprites = c.Group()
        self.item_sprites = c.Group()
        self.pearl_sprites = c.Group()
        self.semi_collision_sprites = c.Group()
        self.tooth_sprites = c.Group()

        self.player = None
        
        self.setup(tmx_map, level_frames)

        # frames
        self.particle_frames = level_frames["particle"]
        self.pearl_frames = level_frames["pearl"]

    def setup(self, tmx_map, level_frames):

        #  tiles
        for layer in ["BG", "Terrain", "FG", "Platforms"]:

            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():

                groups = [self.all_sprites]

                if layer == "Platforms":

                    groups.append(self.semi_collision_sprites)

                if layer == "Terrain":

                    groups.append(self.collision_sprites)

                match layer:

                    case "BG": z = c.Z_LAYERS["bg_tiles"]

                    case "FG": z = c.Z_LAYERS["bg_tiles"]

                    case _: z = c.Z_LAYERS["main"]

                s.CustomSprite((x * c.TILE_SIZE, y * c.TILE_SIZE), groups, surface, z)

        # background details
        for thing in tmx_map.get_layer_by_name("BG details"):

            if thing.name == "static":

                s.CustomSprite((thing.x, thing.y), self.all_sprites, thing.image, c.Z_LAYERS["bg_tiles"])

            else:

                s.AnimatedSprite(
                    level_frames[thing.name],
                    self.all_sprites,
                    (thing.x, thing.y),
                    c.Z_LAYERS["bg_tiles"]
                )

                if thing.name == "candle":

                    s.AnimatedSprite(
                        level_frames["candle_light"],
                        self.all_sprites,
                        (thing.x, thing.y) + c.Vector2(-20, -20),
                        c.Z_LAYERS["bg_tiles"]
                    )

        #  objects
        for thing in tmx_map.get_layer_by_name("Objects"):

            if thing.name == "player":

                self.player = Player(
                    collision_sprites=self.collision_sprites,
                    data=self.data,
                    frames=level_frames["player"],
                    groups=self.all_sprites,
                    position=(thing.x, thing.y),
                    semi_collision_sprites=self.semi_collision_sprites,
                )

            else:

                if thing.name in ("barrel", "crate"):

                    s.CustomSprite((thing.x, thing.y), (self.all_sprites, self.collision_sprites), thing.image)

                else:

                    # frames
                    if "palm" not in thing.name:

                        frames = level_frames[thing.name]

                    else:

                        frames = level_frames["palm"][thing.name]

                    if thing.name == "floor_spike" and thing.properties["inverted"]:

                        frames = [c.flip(frame, False, True) for frame in frames]

                    # groups
                    groups = [self.all_sprites]

                    if thing.name in ("palm_large", "palm_small"):

                        groups.append(self.semi_collision_sprites)

                    if thing.name in ("floor_spike", "saw"):

                        groups.append(self.damage_sprites)

                    # z index
                    z = c.Z_LAYERS["main"] if "bg" not in thing.name else c.Z_LAYERS["bg_details"]

                    # animation speed
                    if "palm" not in thing.name:

                        animation_speed = c.ANIMATION_SPEED

                    else:

                        animation_speed = c.ANIMATION_SPEED + c.uniform(-1, 1)

                    s.AnimatedSprite(frames, groups, (thing.x, thing.y), animation_speed, z)

            if thing.name == "flag":

                self.level_finish_rectangle = c.FRect((thing.x, thing.y), (thing.width, thing.height))
        
        #  moving objects
        for thing in tmx_map.get_layer_by_name("Moving Objects"):

            if thing.name == "spike":

                # position, surface
                s.SpikedSprite(
                    start_angle=thing.properties["start_angle"],
                    end_angle=thing.properties["end_angle"],
                    groups=(self.all_sprites, self.damage_sprites),
                    position=(thing.x + thing.width / 2, thing.y + thing.height / 2),
                    radius=thing.properties["radius"],
                    speed=thing.properties["speed"],
                    surface=level_frames["ball_spike"]
                )

                for radius in range(0, thing.properties["radius"], 20):

                    s.SpikedSprite(
                        start_angle=thing.properties["start_angle"],
                        end_angle=thing.properties["end_angle"],
                        groups=self.all_sprites,
                        position=(thing.x + thing.width / 2, thing.y + thing.height / 2),
                        radius=radius,
                        speed=thing.properties["speed"],
                        surface=level_frames["spike_chain"],
                        z=c.Z_LAYERS["bg_details"]
                    )

            else:

                frames = level_frames[thing.name]

                if thing.properties["platform"]:

                    groups = (self.all_sprites, self.semi_collision_sprites)

                else:

                    groups = (self.all_sprites, self.damage_sprites)

                if thing.width > thing.height:  # horizontal

                    move_direction = "x"
                    start_position = (
                        thing.x,
                        thing.y + thing.height / 2
                    )
                    end_position = (
                        thing.x + thing.width,
                        thing.y + thing.height / 2
                    )

                else:  # vertical

                    move_direction = "y"
                    start_position = (
                        thing.x + thing.width / 2,
                        thing.y
                    )
                    end_position = (
                        thing.x + thing.width / 2,
                        thing.y + thing.height
                    )

                speed = thing.properties["speed"]

                s.MovingSprite(
                    frames=frames,
                    groups=groups,
                    move_direction=move_direction,
                    start_position=start_position,
                    end_position=end_position,
                    speed=speed,
                    flip_image=thing.properties["flip"]
                )

                if thing.name == "saw":

                    if move_direction == "x":

                        y = start_position[1] - level_frames["saw_chain"].get_height() / 2
                        left = int(start_position[0])
                        right = int(end_position[0])

                        for x in range(left, right, 20):

                            s.CustomSprite(
                                (x, y),
                                self.all_sprites,
                                level_frames["saw_chain"],
                                c.Z_LAYERS["bg_details"]
                            )

                    else:

                        x = start_position[0] - level_frames["saw_chain"].get_width() / 2
                        top = int(start_position[1])
                        bottom = int(end_position[1])

                        for y in range(top, bottom, 20):

                            s.CustomSprite(
                                (x, y),
                                self.all_sprites,
                                level_frames["saw_chain"],
                                c.Z_LAYERS["bg_details"]
                            )

        # enemies
        for thing in tmx_map.get_layer_by_name("Enemies"):

            if thing.name == "tooth":

                Tooth(
                    self.collision_sprites,
                    level_frames["tooth"],
                    (self.all_sprites, self.collision_sprites, self.tooth_sprites),
                    (thing.x, thing.y)
                )

            if thing.name == "shell":

                Shell(
                    create_pearl=self.create_pearl,
                    frames=level_frames["shell"],
                    groups=(self.all_sprites, self.collision_sprites),
                    player=self.player,
                    position=(thing.x, thing.y),
                    reverse=thing.properties["reverse"]
                )

        # items
        for thing in tmx_map.get_layer_by_name("Items"):

            s.ItemSprite(
                data=self.data,
                frames=level_frames["item"][thing.name],
                groups=(self.all_sprites, self.item_sprites),
                item_type=thing.name,
                position=(thing.x + c.TILE_SIZE / 2, thing.y + c.TILE_SIZE / 2)
            )

        # water
        for thing in tmx_map.get_layer_by_name("Water"):

            rows = int(thing.height / c.TILE_SIZE)
            columns = int(thing.width / c.TILE_SIZE)

            for row in range(rows):

                for column in range(columns):

                    x = thing.x + column * c.TILE_SIZE
                    y = thing.y + row * c.TILE_SIZE

                    if row == 0:

                        s.AnimatedSprite(
                            frames=level_frames["water top"],
                            groups=self.all_sprites,
                            position=(x, y),
                            animation_speed=c.ANIMATION_SPEED,
                            z=c.Z_LAYERS["water"]
                        )

                    else:

                        s.CustomSprite(
                            (x, y),
                            self.all_sprites,
                            level_frames["water body"],
                            c.Z_LAYERS["water"]
                        )

    def create_pearl(self, direction, position):

        Pearl(
            direction,
            (self.all_sprites, self.damage_sprites, self.pearl_sprites),
            position,
            150,
            self.pearl_frames
        )

    def pearl_collision(self):

        for sprite in self.collision_sprites:

            sprite = c.spritecollide(sprite, self.pearl_sprites, True)

            if sprite:

                s.ParticleEffectSprite(self.particle_frames, self.all_sprites, sprite[0].rect.center)

    def hit_collision(self):

        for sprite in self.damage_sprites:

            if sprite.rect.colliderect(self.player.hit_box_rectangle):

                self.player.get_damage()
                
                if hasattr(sprite, "pearl"):

                    sprite.kill()
                    s.ParticleEffectSprite(self.particle_frames, self.all_sprites, sprite.rect.center)

    def item_collision(self):

        if self.item_sprites:

            item_sprites = c.spritecollide(self.player, self.item_sprites, True)

            if item_sprites:

                item_sprites[0].activate()
                s.ParticleEffectSprite(self.particle_frames, self.all_sprites, item_sprites[0].rect.center)

    def attack_collision(self):

        for target in self.pearl_sprites.sprites() + self.tooth_sprites.sprites():

            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or \
                            self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            
            if (
                target.rect.colliderect(self.player.rect) and
                self.player.interacting and
                facing_target
            ):

                target.reverse()

    def check_constraint(self):

        # bottom
        if self.player.hit_box_rectangle.bottom > self.level_bottom:

            self.player.hit_box_rectangle.bottom = self.level_bottom
        
        # left
        if self.player.hit_box_rectangle.left <= 0:

            self.player.hit_box_rectangle.left = 0

        # right
        if self.player.hit_box_rectangle.right >= self.level_right:

            self.player.hit_box_rectangle.right = self.level_right

        # success
        if self.player.hit_box_rectangle.colliderect(self.level_finish_rectangle):

            pass

    def run(self, delta_time):

        self.surface.fill("black")

        self.all_sprites.update(delta_time)
        self.pearl_collision()
        self.hit_collision()
        self.item_collision()
        self.check_constraint()

        self.all_sprites.draw(delta_time, self.player.hit_box_rectangle.center)
