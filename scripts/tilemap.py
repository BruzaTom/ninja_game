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

    def render(self, surface):
        #
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile_type][tile_variant], tile_pos)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            tile_type = tile['type']
            tile_variant = tile['variant']
            tile_pos = tile['pos']
            surface.blit(self.game.assets[tile_type][tile_variant], (tile_pos[0] * self.tile_size, tile_pos[1] * self.tile_size))


