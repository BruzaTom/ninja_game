import sys
import random#partickles
import math#particles
import pygame
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import TileMap
from scripts.clouds import Clouds
from scripts.particle import Particle

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('ninja game')
        #game screen
        self.screen = pygame.display.set_mode((640, 480))
        #render size 'zoom'
        self.display = pygame.Surface((320, 240))
        #
        self.clock = pygame.time.Clock()
        #movement x y
        self.movement = [False, False]

        self.assets = {
                #from scripts/utils.py
                'decor' : load_images('tiles/decor'),
                'grass' : load_images('tiles/grass'),
                'large_decor' : load_images('tiles/large_decor'),
                'stone' : load_images('tiles/stone'),
                'player' : load_image('entities/player.png'),
                'background' : load_image('background.png'),
                'clouds': load_images('clouds'),
                'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
                'player/run': Animation(load_images('entities/player/run'), img_dur=4),
                'player/jump': Animation(load_images('entities/player/jump'), img_dur=4),
                'player/slide': Animation(load_images('entities/player/slide'), img_dur=4),
                'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur=4),
                'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
                }
        #print(self.assets)

        self.clouds = Clouds(self.assets['clouds'], count=16)
        #from scripts/entities.py
        self.player = Player(self, (50, 50), (8, 15))

        #pass in assets to TileMap using self as the game
        self.tilemap = TileMap(self, tile_size=16)
        self.tilemap.load('map.json')
        
        #particles
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.particles = []

        #camera scroll
        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))
            #scroll
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            #convert to int to avoid jitters
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            #spawn particals
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos_x = rect.x + random.random() * rect.width
                    pos_y = rect.y + random.random() * rect.height
                    pos = (pos_x, pos_y)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            #player entity calls
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            self.tilemap.render(self.display, offset=render_scroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            
            #manage particles
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.p_type == 'leaf':
                    #apply sin effect to position               0.035 slows down effect
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)
                
            #print(self.tilemap.physics_rects_around(self.player.pos))
            #input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            #finishers
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()
