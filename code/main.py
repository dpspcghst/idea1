import core as c
from data import Data
from debug import debug
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    """
    The main game class. What we think of when we think of the game.
    """

    def __init__(self):
        """
        Happens when the game is started.
        """

        c.pygame.init()  # starts the Pygame engine
        
        # creates the game window depending on determined width and height
        self.surface = c.set_mode(
            (c.WINDOW_WIDTH, c.WINDOW_HEIGHT)
        )
        c.set_caption("Zone")
        self.clock = c.Clock()
        self.level_frames = None
        self.import_assets()  # change to c.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        # loads the individual levels
        self.tmx_maps = {
            0: c.load_engine(c.join("..", "data", "levels", "0.tmx")),
            1: c.load_engine(c.join("..", "data", "levels", "1.tmx")),
            2: c.load_engine(c.join("..", "data", "levels", "2.tmx")),
            3: c.load_engine(c.join("..", "data", "levels", "3.tmx")),
            4: c.load_engine(c.join("..", "data", "levels", "4.tmx")),
            5: c.load_engine(c.join("..", "data", "levels", "5.tmx"))
        }
        self.tmx_overworld = c.load_engine(c.join("..", "data", "overworld", "overworld.tmx"))
        self.current_stage = Level(self.data, self.level_frames, self.switch_stage, self.tmx_maps[0])
        """
        This takes the levels made in Tiled and passes them though the level class. The
        level class is what's doing the bulk of the work in this game.
        """

    def switch_stage(self, target, unlock = 0):

        if target == "level":

            # self.current_stage = Level()
            pass

        else:  # overworld

            if unlock > 0:

                self.data.unlocked_level = unlock

            else:

                self.data.health -= 1
                
            self.current_stage = Overworld(self.data, self.overworld_frames, self.switch_stage, self.tmx_overworld)
        
    def import_assets(self):
        """
        This is probably going to get moved to core.
        """

        self.level_frames = {
            "ball_spike": c.import_image("..", "graphics", "enemies", "ball_spike", "ball_spike"),
            "bg_tile": c.import_folder_dictionary("..", "graphics", "level", "bg", "tiles"),
            "big_chain": c.import_folder("..", "graphics", "level", "big_chains"),
            "big_cloud": c.import_image("..", "graphics", "level", "clouds", "big_cloud"),
            "boat": c.import_folder("..", "graphics", "objects", "boat"),
            "candle": c.import_folder("..", "graphics", "level", "candle"),
            "candle_light": c.import_folder("..", "graphics", "level", "candle_light"),
            "flag": c.import_folder("..", "graphics", "level", "flag"),
            "floor_spike": c.import_folder("..", "graphics", "enemies", "floor_spikes"),
            "helicopter": c.import_folder("..", "graphics", "level", "helicopter"),
            "item": c.import_sub_folders("..", "graphics", "items"),
            "palm": c.import_sub_folders("..", "graphics", "level", "palms"),
            "particle": c.import_folder("..", "graphics", "effects", "particle"),
            "pearl": c.import_image("..", "graphics", "enemies", "bullets", "pearl"),
            "player": c.import_sub_folders("..", "graphics", "player"),
            "saw": c.import_folder("..", "graphics", "enemies", "saw", "animation"),
            "saw_chain": c.import_image("..", "graphics", "enemies", "saw", "saw_chain"),
            "shell": c.import_sub_folders("..", "graphics", "enemies", "shell"),
            "small_chain": c.import_folder("..", "graphics", "level", "small_chains"),
            "small_cloud": c.import_folder("..", "graphics", "level", "clouds", "small"),
            "spike_chain": c.import_image("..", "graphics", "enemies", "ball_spike", "spike_chain"),
            "tooth": c.import_folder("..", "graphics", "enemies", "tooth", "run"),
            "water body": c.import_image("..", "graphics", "level", "water", "body"),
            "water top": c.import_folder("..", "graphics", "level", "water", "top"),
            "window": c.import_folder("..", "graphics", "level", "window")
        }

        self.font = c.Font(c.join("..", "graphics", "ui", "runescape_uf.ttf"), 40)
        self.ui_frames = {
            "coin": c.import_image("..", "graphics", "ui", "coin"),
            "heart": c.import_folder("..", "graphics", "ui", "heart")
        }

        self.overworld_frames = {
            "icon": c.import_sub_folders("..", "graphics", "overworld", "icon"),
            "palm": c.import_folder("..", "graphics", "overworld", "palm"),
            "path": c.import_folder_dictionary("..", "graphics", "overworld", "paths"),
            "water": c.import_folder("..", "graphics", "overworld", "water")
        }
    
    def run(self):
        """
        Happens while the game is running.
        """

        # previous_time = c.get_ticks()

        while c.RUNNING:

            # creating delta time and setting the frame rate
            delta_time = self.clock.tick(30) / 1000

            """
            Return to following delta timing on a better machine.
            """
            # current_time = c.get_ticks()
            # dt = (current_time - previous_time) / 1000
            # print(dt)
            # previous_time = current_time

            for event in c.get():

                if event.type == c.pygame.QUIT:

                    c.quit()
                    c.exit()

            # runs the level class with the delta time
            self.current_stage.run(delta_time)
            self.ui.update(delta_time)
            c.update()  # updates the game
            # self.clock.tick(30)


if __name__ == "__main__":
    """
    Only works if the file's name is 'main'.
    """

    game = Game()  # starts the game
    game.run()  # runs the game
