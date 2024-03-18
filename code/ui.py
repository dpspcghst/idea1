import core as c
from sprites import AnimatedSprite
from timer import Timer

class UI:

    def __init__(self, font, frames, ):

        self.surface = c.get_surface()
        self.sprites = c.Group()
        self.font = font

        # health / hearts
        self.heart_frames = frames["heart"]
        self.heart_surface_width = self.heart_frames[0].get_width()
        self.heart_padding = 5

        # coins
        self.coin_amount = 0
        self.coin_timer = Timer(1000)
        self.coin_surface = frames["coin"]

    def create_hearts(self, amount):

        for sprite in self.sprites:

            sprite.kill()
        
        for heart in range(amount):

            x = 10 + heart * (self.heart_surface_width + self.heart_padding)
            y = 10
            
            Heart(self.heart_frames, self.sprites, (x, y))

    def display_text(self):

        if self.coin_timer.active:

            text_surface = self.font.render(str(self.coin_amount), False, "#33323d")
            text_rectangle = text_surface.get_frect(topleft=(16, 34))
            self.surface.blit(text_surface, text_rectangle)

            coin_rectangle = self.coin_surface.get_frect(center=text_rectangle.bottomleft).move(0, -6)
            self.surface.blit(self.coin_surface, coin_rectangle)
    
    def show_coins(self, amount):

        self.coin_amount = amount
        self.coin_timer.activate()
    
    def update(self, delta_time):

        self.coin_timer.update()
        self.sprites.update(delta_time)
        self.sprites.draw(self.surface)
        self.display_text()

class Heart(AnimatedSprite):

    def __init__(self, frames, groups, position):

        super().__init__(frames, groups, position)
        self.active = False

    def animate(self, delta_time):

        self.frame_index += c.ANIMATION_SPEED * delta_time

        if self.frame_index < len(self.frames):

            self.image = self.frames[int(self.frame_index)]

        else:

            self.active = False
            self.frame_index = 0
    
    def update(self, delta_time):

        if self.active:

            self.animate(delta_time)

        else:

            if c.randint(0, 2000) == 1:

                self.active = True
