import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        #if using baisic py not pyce
        self.pos = list(pos)#force convert list
        self.size = size
        self.velocity = [0, 0]
        #keep track of collisions, usefule like walljumnping
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.ani_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        self.last_movement = [0, 0]

    def set_action(self, action):
        if action != self.action:
            self.action = action
            #set animation object from game
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        #keep track of collisions, usefule like walljumnping
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        #movement and collisions work togethr
        #check rects around player x pos for collisions
        #then move player pos if possible
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        #check rects around player y pos for collisions
        self.pos[1] += frame_movement[1]
        #new entity_rect or else dosent work
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        #animation flip
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        #gravity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surface, offset=(0, 0)):
        flip_flagged_img = pygame.transform.flip(self.animation.img(), self.flip, False)
        pos_offset_p_ani_x = self.pos[0] - offset[0] + self.ani_offset[0] 
        pos_offset_p_ani_y = self.pos[1] - offset[1] + self.ani_offset[1] 
        ani_pos_os = (pos_offset_p_ani_x, pos_offset_p_ani_y) 
        surface.blit(flip_flagged_img, ani_pos_os)
       
       #before animations
        #surface.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
            
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1
        
        #conditions for wall_slide
        l_r_collide = (self.collisions['right'] or self.collisions['left'])
        in_air = self.air_time > 4 
        falling = self.velocity[1] > 0 
        #(if hit wall on either side) and (in the air and falling)
        if l_r_collide and (in_air and falling):
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')
        #else no wall_slide
        else:
            self.wall_slide = False

        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                #trigger jump animation
                self.air_time = 5
                #ensure that jumps dosent fall below 0
                self.jumps = max(0, self.jumps - 1)
                #handy return true to hook on some functinality possibly
                return True
            if not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.airtime = 5
            return True



