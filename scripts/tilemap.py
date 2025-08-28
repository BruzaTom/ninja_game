import json
import pygame

AUTOTILE_MAP = {
        #if tile right and below use tile 0
        tuple(sorted([(1, 0), (0, 1)])): 0,#sorted for consistancy and tuple for key-value
        #right, below, and to left
        tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
        #left, below
        tuple(sorted([(-1, 0), (0, 1)])): 2,
        #left, above, below
        tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
        #left, above
        tuple(sorted([(-1, 0), (0, -1)])): 4,
        #left, above, right
        tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
        #right, above
        tuple(sorted([(1, 0), (0, -1)])): 6,
        #right, above, below
        tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
        #all
        tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8
        }
#variable for tile locations around player
NEIGHBORS_OFFSETS = [(-1, 0), (-1,-1), (0,-1), (1,-1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}
AUTOTILE_TYPES = {'grass', 'stone'} 

class TileMap:
    def __init__(self, game,tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []


        # the tiles will be saved as strings of dictionary values

    def tiles_around(self, pos):
        tiles = []
        #
        tile_loc_x = int(pos[0] // self.tile_size)
        tile_loc_y = int(pos[1] // self.tile_size) 
        tile_loc = (tile_loc_x, tile_loc_y)#tuple..
        for offset in NEIGHBORS_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    #makes tile editor eaiser to work with
    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            #exclude diagnals from offset neighbors
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]
                    

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    
    #save to json
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                tile_pos_x_by_size = tile['pos'][0] * self.tile_size 
                tile_pos_y_by_size = tile['pos'][1] * self.tile_size 
                rects.append(pygame.Rect(tile_pos_x_by_size, tile_pos_y_by_size, self.tile_size, self.tile_size))
        return rects


    def render(self, surface, offset=(0, 0)):
        #
        #tilemap blits
        for tile in self.offgrid_tiles:
            tile_type = tile['type']
            tile_variant = tile['variant']
            tile_pos = tile['pos']
            tile_pos_offset = (tile_pos[0] - offset[0], tile_pos[1] - offset[1]) 
            img = self.game.assets[tile_type][tile_variant] 
            surface.blit(img, tile_pos_offset)

        #x range lookup
        start_x = offset[0] // self.tile_size
        end_x = (offset[0] + surface.get_width()) // self.tile_size + 1
        #y range lookup
        start_y = offset[1] // self.tile_size
        end_y = (offset[1] + surface.get_height()) // self.tile_size + 1
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    tile_type = tile['type']
                    tile_variant = tile['variant']
                    tile_pos = tile['pos']
                    tile_pos_x_os = tile_pos[0] * self.tile_size - offset[0] 
                    tile_pos_y_os = tile_pos[1] * self.tile_size - offset[1] 
                    tile_pos_offset = (tile_pos_x_os, tile_pos_y_os) 
                    img = self.game.assets[tile_type][tile_variant] 
                    surface.blit(img, tile_pos_offset)
            

        #for loc in self.tilemap:
            #tile = self.tilemap[loc]
            #tile_type = tile['type']
            #tile_variant = tile['variant']
            #tile_pos = tile['pos']
            #surface.blit(self.game.assets[tile_type][tile_variant], (tile_pos[0] * self.tile_size - offset[0], tile_pos[1] * self.tile_size - offset[1]))


