import core as c
from groups import WorldSprites
import sprites as s

class Overworld:

    def __init__(self, data, overworld_frames, tmx_map):

        self.surface = c.get_surface()
        self.data = data

        # groups
        self.all_sprites = WorldSprites(data)
        self.node_sprites = c.Group()

        self.setup(overworld_frames, tmx_map)

        self.current_node = [node for node in self.node_sprites if node.level == 0][0]

        self.path_frames = overworld_frames["path"]
        self.create_path_sprites()

    def setup(self, overworld_frames, tmx_map):

        # tiles
        for layer in ["main", "top"]:

            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():

                s.CustomSprite(
                    (x * c.TILE_SIZE, y * c.TILE_SIZE),
                    self.all_sprites,
                    surface,
                    c.Z_LAYERS["bg_tiles"]
                )

        # water
        for column in range(tmx_map.width):

            for row in range(tmx_map.height):

                s.AnimatedSprite(
                    frames=overworld_frames["water"],
                    groups=self.all_sprites,
                    position=(column * c.TILE_SIZE, row * c.TILE_SIZE),
                    animation_speed=c.ANIMATION_SPEED,
                    z=c.Z_LAYERS["bg"])

        # things
        for thing in tmx_map.get_layer_by_name("Objects"):

            if thing.name == "palm":

                s.AnimatedSprite(
                    frames=overworld_frames["palm"],
                    groups=self.all_sprites,
                    position=(thing.x, thing.y),
                    animation_speed=c.randint(3,7),
                    z=c.Z_LAYERS["main"])

            else:

                if thing.name == "grass":
                    
                    z = c.Z_LAYERS["bg_details"]

                else:

                    z = c.Z_LAYERS["bg_tiles"]

                s.CustomSprite((thing.x, thing.y), self.all_sprites, thing.image, z)

        # paths
        self.paths = {}
        for thing in tmx_map.get_layer_by_name("Paths"):

            position = [(int(p.x + c.TILE_SIZE / 2), int(p.y + c.TILE_SIZE / 2)) for p in thing.points]
            start = thing.properties["start"]
            end = thing.properties["end"]
            self.paths[end] = {"position": position, "start": start}
        
        # nodes & player
        for thing in tmx_map.get_layer_by_name("Nodes"):

            # player
            if thing.name == "Node" and thing.properties["stage"] == self.data.current_level:

                self.icon = s.IconSprite(
                    overworld_frames["icon"],
                    self.all_sprites,
                    (thing.x + c.TILE_SIZE / 2, thing.y + c.TILE_SIZE / 2)
                )
            
            # nodes
            if thing.name == "Node":

                available_paths = {k:v for k,v in thing.properties.items() if k in ("down", "left", "right", "up")}
                
                s.NodeSprite(
                    data=self.data,
                    groups=(self.all_sprites, self.node_sprites),
                    level=thing.properties["stage"],
                    paths=available_paths,
                    position=(thing.x, thing.y),
                    surface=overworld_frames["path"]["node"]
                )

    def create_path_sprites(self):

        # get tiles from path
        nodes = {node.level: c.Vector2(node.grid_position) for node in self.node_sprites}
        path_tiles = {}

        for path_id, data in self.paths.items():

            path = data["position"]
            start_node = nodes[data["start"]]
            end_node = nodes[path_id]
            path_tiles[path_id] = [start_node]

            for index, points in enumerate(path):

                if index < len(path) - 1:

                    start = c.Vector2(points)
                    end = c.Vector2(path[index + 1])
                    path_direction = (end - start) / c.TILE_SIZE
                    start_tile = c.Vector2(int(start[0] / c.TILE_SIZE), int(start[1] / c.TILE_SIZE))

                    if path_direction.y:

                        direction_y = 1 if path_direction.y > 0 else -1

                        for y in range(direction_y, int(path_direction.y) + direction_y, direction_y):

                            path_tiles[path_id].append(start_tile + c.Vector2(0, y))

                    if path_direction.x:

                        direction_x = 1 if path_direction.x > 0 else -1

                        for x in range(direction_x, int(path_direction.x) + direction_x, direction_x):

                            path_tiles[path_id].append(start_tile + c.Vector2(x, 0))
            
            path_tiles[path_id].append(end_node)
    
        # create sprites
        for key, path in path_tiles.items():

            for index, tile in enumerate(path):

                if index > 0 and index < len(path) - 1:

                    previous_tile = path[index - 1] - tile
                    next_tile = path[index + 1] - tile
                    surface = c.Surface((c.TILE_SIZE, c.TILE_SIZE))
                    
                    if previous_tile.x == next_tile.x:

                        surface = self.path_frames["vertical"]

                    elif previous_tile.y == next_tile.y:

                        surface = self.path_frames["horizontal"]

                    s.PathSprite(
                        groups=self.all_sprites,
                        level=key,
                        position=(tile.x * c.TILE_SIZE, tile.y * c.TILE_SIZE),
                        surface=surface
                    )
            
    def input(self):

        keys = c.get_pressed()
        # input_vector = c.Vector2(0, 0)

        if self.current_node and not self.icon.path:

            if keys[c.pygame.K_DOWN] and self.current_node.can_move("down"):
    
                self.move("down")
            
            if keys[c.pygame.K_LEFT] and self.current_node.can_move("left"):
    
                self.move("left")
            
            if keys[c.pygame.K_RIGHT] and self.current_node.can_move("right"):
    
                self.move("right")
    
            if keys[c.pygame.K_UP] and self.current_node.can_move("up"):
    
                self.move("up")
    
    def move(self, direction):

        path_key = int(self.current_node.paths[direction][0])
        path_reverse = True if self.current_node.paths[direction][-1] == "r" else False

        if not path_reverse:
            
            path = self.paths[path_key]["position"][:]
            
        else:
            
            path = self.paths[path_key]["position"][::-1]

        self.icon.start_move(path)
    
    def get_current_node(self):

        nodes = c.spritecollide(self.icon, self.node_sprites, False)

        if nodes:

            self.current_node = nodes[0]
                
    def run(self, delta_time):

        self.input()
        self.get_current_node()
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.icon.rect.center)
