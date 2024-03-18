import core as c


class Timer:

    def __init__(self, duration, function=None, repeat=False):

        self.duration = duration
        self.function = function
        self.start_time = 0
        self.active = False
        self.repeat = repeat

    def activate(self):

        self.active = True
        self.start_time = c.get_ticks()

    def deactivate(self):

        self.active = False
        self.start_time = 0

        if self.repeat:

            self.activate()

    def update(self):

        current_time = c.get_ticks()

        if current_time - self.start_time >= self.duration:

            if self.function and self.start_time != 0:

                self.function()

            self.deactivate()
