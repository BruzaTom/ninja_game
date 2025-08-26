import pygame
#variable for tile locations around player
NEIGHBORS_OFFSETS = [(-1, 0), (-1,-1), (0,-1), (1,-1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}

class TileMap:
    def __init__(self, game,tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []


        # the tiles will be saved as strings of dictionary values
        for i in range(0, 10):
            #x for tile map
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            #y for tile map
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}


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

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects


    def render(self, surface, offset=(0, 0)):
        #
        #tilemap blits
        for tile in self.offgrid_tiles:
            tile_type = tile['type']
            tile_variant = tile['variant']
            tile_pos = tile['pos']
            surface.blit(self.game.assets[tile_type][tile_variant], (tile_pos[0] - offset[0], tile_pos[1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width())  // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height())  // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    tile_type = tile['type']
                    tile_variant = tile['variant']
                    tile_pos = tile['pos']
                    surface.blit(self.game.assets[tile_type][tile_variant], (tile_pos[0] * self.tile_size - offset[0], tile_pos[1] * self.tile_size - offset[1]))
            

        #for loc in self.tilemap:
            #tile = self.tilemap[loc]
            #tile_type = tile['type']
            #tile_variant = tile['variant']
            #tile_pos = tile['pos']
            #surface.blit(self.game.assets[tile_type][tile_variant], (tile_pos[0] * self.tile_size - offset[0], tile_pos[1] * self.tile_size - offset[1]))


