import core as c
from timer import Timer


class Player(c.Sprite):

    def __init__(self, collision_sprites, data, frames, groups, position, semi_collision_sprites):

        # general setup
        super().__init__(groups)
        self.z = c.Z_LAYERS["main"]
        self.data = data

        # image
        self.frames = frames
        self.frame_index = 0
        self.state = "idle"
        self.facing_right = True
        self.image = self.frames[self.state][self.frame_index]

        #  rects
        self.rect = self.image.get_frect(topleft=position)
        self.hit_box_rectangle = self.rect.inflate(-76, -36)
        self.old_rect = self.hit_box_rectangle.copy()

        #  movement
        self.direction = c.Vector2()
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jump_height = 675
        self.interacting = False

        #  collision
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {"floor": False, "left": False, "right": False}
        self.platform = None

        #  timers
        self.timers = {
            "hit": Timer(400),
            "interact block": Timer(500),
            "platform skip": Timer(100),
            "wall jump": Timer(400),
            "wall slide block": Timer(250)
        }

    def input(self):

        keys = c.get_pressed()
        input_vector = c.Vector2(0, 0)

        if not self.timers["wall jump"].active:

            if keys[c.pygame.K_DOWN]:
    
                self.timers["platform skip"].activate()
            
            if keys[c.pygame.K_LEFT]:
    
                input_vector.x -= 1
                self.facing_right = False
            
            if keys[c.pygame.K_RIGHT]:
    
                input_vector.x += 1
                self.facing_right = True
    
            if keys[c.pygame.K_UP]:
    
                input_vector.y -= 1

            if keys[c.pygame.K_x]:

                self.interact()
        
            if input_vector:
                
                self.direction.x = input_vector.normalize().x
                
            else:
                
                self.direction.x = 0

        if keys[c.pygame.K_SPACE]:

            self.jump = True

    def interact(self):

        if not self.timers["interact block"].active:

            self.interacting = True
            self.frame_index = 0
            self.timers["interact block"].activate()
            
    def move(self, delta_time):

        #  horizontal
        self.hit_box_rectangle.x += self.direction.x * self.speed * delta_time
        self.collision("horizontal")
        
        #  vertical
        if (
            not self.on_surface["floor"] and
            any((self.on_surface["left"], self.on_surface["right"])) and
            self.timers["wall slide block"].active
        ):

            self.direction.y = 0
            self.hit_box_rectangle.y += self.gravity / 10 * delta_time
            
        else:

            self.direction.y += self.gravity / 2 * delta_time
            self.hit_box_rectangle.y += self.direction.y * delta_time
            self.direction.y += self.gravity / 2 * delta_time

        if self.jump:

            if self.on_surface["floor"]:

                self.direction.y = -self.jump_height
                self.timers["wall slide block"].activate()
                self.hit_box_rectangle.bottom -= 1

            elif (
                  any((self.on_surface["left"], self.on_surface["right"])) and not 
                  self.timers["wall slide block"].active
            ):

                self.timers["wall jump"].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface["left"] else -1

            self.jump = False

        self.collision("vertical")
        self.semi_collision()
        self.rect.center = self.hit_box_rectangle.center

    def platform_move(self, delta_time):

        if self.platform:

            self.hit_box_rectangle.topleft += self.platform.direction * self.platform.speed * delta_time
    
    def check_contact(self):

        # ceiling_rectangle = c.pygame.Rect(self.rect.topleft, (self.rect.width, -2))
        floor_rectangle = c.pygame.Rect(self.hit_box_rectangle.bottomleft, (self.hit_box_rectangle.width, 2))
        left_rectangle = c.pygame.Rect(self.rect.topleft, (-2, self.rect.height))
        right_rectangle = c.pygame.Rect(self.rect.topright, (2, self.rect.height))
        collide_rectangles = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rectangles = [sprite.rect for sprite in self.semi_collision_sprites]

        #  collisions
        if (
            floor_rectangle.collidelist(collide_rectangles) >= 0 or
            floor_rectangle.collidelist(semi_collide_rectangles) >= 0 and
            self.direction.y >= 0
        ):

            self.on_surface["floor"] = True

        else:

            self.on_surface["floor"] = False

        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()

        for sprite in [sprite for sprite in sprites if hasattr(sprite, "moving")]:

            if sprite.rect.colliderect(floor_rectangle):

                self.platform = sprite
    
    def collision(self, axis):

        for sprite in self.collision_sprites:

            if sprite.rect.colliderect(self.hit_box_rectangle):

                if axis == "horizontal":

                    #  left
                    if (
                        self.hit_box_rectangle.left <= sprite.rect.right and
                        int(self.old_rect.left) >= int(sprite.old_rect.right)
                    ):

                        self.hit_box_rectangle.left = sprite.rect.right

                    #  right
                    if (
                        self.hit_box_rectangle.right >= sprite.rect.left and
                        int(self.old_rect.right) <= int(sprite.old_rect.left)
                    ):

                        self.hit_box_rectangle.right = sprite.rect.left

                else:  # vertical

                    #  bottom
                    if (
                        self.hit_box_rectangle.bottom >= sprite.rect.top and
                        int(self.old_rect.bottom) <= int(sprite.old_rect.top)
                    ):

                        self.hit_box_rectangle.bottom = sprite.rect.top

                    #  top
                    if (
                        self.hit_box_rectangle.top <= sprite.rect.bottom and
                        int(self.old_rect.top) >= int(sprite.old_rect.bottom)
                    ):

                        self.hit_box_rectangle.top = sprite.rect.bottom

                        if hasattr(sprite, "moving"):

                            self.hit_box_rectangle.top += 6

                    self.direction.y = 0
    
    def semi_collision(self):

        if not self.timers["platform skip"].active:

            for sprite in self.semi_collision_sprites:
    
                if sprite.rect.colliderect(self.hit_box_rectangle):
    
                    if (
                            self.hit_box_rectangle.bottom >= sprite.rect.top and
                            int(self.old_rect.bottom) <= int(sprite.old_rect.top)
                    ):
    
                        self.hit_box_rectangle.bottom = sprite.rect.top
                            
                        if self.direction.y > 0:
                                
                            self.direction.y = 0
    
    def update_timers(self):

        for timer in self.timers.values():

            timer.update()
    
    def animate(self, delta_time):

        self.frame_index += c.ANIMATION_SPEED * delta_time

        if self.state == "attack" and self.frame_index >= len(self.frames[self.state]):

            self.state = "idle"

        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else c.flip(self.image, True, False)

        if self.interacting and self.frame_index > len(self.frames[self.state]):

            self.interacting = False
    
    def get_state(self):

        if self.on_surface["floor"]:

            if self.interacting:
                
                self.state = "attack"
                
            else:
                
                self.state = "idle" if self.direction.x == 0 else "run"

        else:

            if self.interacting:
                
                self.state = "air_attack"

            else:
            
                if any((self.on_surface["left"], self.on_surface["right"])):
    
                    self.state = "wall"
    
                else:
    
                    self.state = "jump" if self.direction.y < 0 else "fall"
    
    def get_damage(self):

        if not self.timers["hit"].active:

            self.data.health -= 1
            self.timers["hit"].activate()
    
    def flicker(self):

        if self.timers["hit"].active and c.sin(c.get_ticks() * 100) >= 0:

            white_mask = c.from_surface(self.image)
            white_surface = white_mask.to_surface()
            white_surface.set_colorkey("black")
            self.image = white_surface
    
    def update(self, delta_time):

        self.old_rect = self.hit_box_rectangle.copy()
        self.update_timers()

        self.input()
        self.move(delta_time)
        self.platform_move(delta_time)
        self.check_contact()

        self.get_state()
        self.animate(delta_time)
        self.flicker()
