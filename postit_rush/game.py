from __future__ import division
from math import ceil
import pygame
import random
from collections import namedtuple
from pygame.locals import *

class World(object):

    def __init__(self, length):
        self.display_size = pygame.display.get_surface().get_size()
        self.length = length
        self.background = _Background(self.length)
        self.map = pygame.rect.Rect( (0, -(self.length - self.display_size[1])), (self.display_size[0], self.length) )
        self.blocks = self._generate_blocks((10, 15))
        self.gems = self._generate_gems(self.blocks, (2, 3))
        self.bug_n_star = self._generate_bug_n_star(n_bugs=20, n_stars=3)

    def _generate_blocks(self, range_per_screen):
        n_blocks = self.length//self.display_size[1] * random.randrange(*range_per_screen)
        blocks = pygame.sprite.Group()
        i = 0
        while i < n_blocks:
            type = random.choice(_Block.types)
            block = _Block( (random.randrange(self.map.left, self.map.right, 50),
                                random.randrange(self.map.top, self.map.bottom, 50)), type )
            if block.rect.collidelist(blocks.sprites()) == -1:
                blocks.add(block)
                i += 1
        return blocks

    def _generate_gems(self, blocks, range_per_screen):
        n_gems = self.length//self.display_size[1] * random.randrange(*range_per_screen)
        gems = pygame.sprite.Group()
        blocks_rects = [block.rect for block in blocks.sprites()]
        for i in xrange(n_gems):
            color = random.choice(_Gem.colors)
            random_block_rect = blocks_rects.pop(random.randrange(len(blocks_rects)))
            coords = (random_block_rect.centerx, random_block_rect.centery-30)
            gems.add(_Gem(coords, color))
        return gems

    def _generate_bug_n_star(self, n_bugs, n_stars):
        bug_n_star = pygame.sprite.Group()
        i = 0
        while i < n_stars:
            star = _Star((random.randrange(self.map.left, self.map.right, 50),
                            random.randrange(self.map.top, self.map.bottom-self.display_size[1], 50)))
            if not pygame.sprite.spritecollideany(star, bug_n_star):
                bug_n_star.add(star)
                i += 1
        i = 0
        while i < n_bugs:
            bug = _Bug(random.randrange(self.map.top, self.map.bottom-self.display_size[1], 50))
            if not pygame.sprite.spritecollideany(bug, bug_n_star):
                bug_n_star.add(bug)
                i += 1
        return bug_n_star

    def destroy(self):
        pass


class _Background(pygame.sprite.Sprite):

    WINDTOLEFT = object()
    WINDTORIGHT = object()

    def __init__(self, world_length):
        super(_Background, self).__init__()
        self._world_length = world_length
        self.display_size = pygame.display.get_surface().get_size()
        self.image = pygame.Surface(self.display_size)
        self.rect = self.image.get_rect()

        cloudy_img = pygame.image.load_extended("postit_rush/asset/graphic/clouds.png")
        self._cloudy_surf = pygame.Surface(self.display_size, SRCALPHA)
        ratio_size = map(lambda x,y: int(ceil(x/y)), self._cloudy_surf.get_size(), cloudy_img.get_size())
        for y in xrange(ratio_size[1]):
            for x in xrange(ratio_size[0]):
                if random.random() > 0.6:
                    coord = (cloudy_img.get_size()[0]*x, cloudy_img.get_size()[1]*y)
                    self._cloudy_surf.blit(cloudy_img, coord)
        self._wind = [0, 0, self.WINDTORIGHT]
        self._wind_to_move = 2
        self._sun_img = pygame.image.load_extended("postit_rush/asset/graphic/sun.png")
        base_color = (9, 74, 223)
        base_sun_coord = (0,0)
        self._sunset_pace = 1
        self._sun_coord = [ (-i, -i) for i in xrange(max(self._sun_img.get_size()), 0, -self._sunset_pace) ]
        self._sunset_colors = []
        self.sunset_duration = 150
        self._base_distance_to_refr = self.distance_to_refresh = world_length/self.sunset_duration
        for i in xrange(0, self.sunset_duration, self._sunset_pace):
            self._sunset_colors.append( (base_color[0]+i, base_color[1]+i, base_color[2]) )

        font = pygame.font.Font("postit_rush/asset/interface/font.ttf", 62)
        self.endtext_1 = font.render("this is the end of this demo!", True, (10, 255, 137))
        self.endtext_2 = font.render("thank you for playing :)", True, (10, 255, 137))

        self.image.fill(self._sunset_colors.pop())
        self.image.blit(self._cloudy_surf, (0,0))
        self.image.blit(self._sun_img, base_sun_coord)

    def update(self, traveled_by_avatar):
        if traveled_by_avatar >= self.distance_to_refresh:
            self.distance_to_refresh += self._base_distance_to_refr
            if self._sunset_colors:
                if self._wind[2]==self.WINDTORIGHT:
                    if self._wind[0] > 40:
                        self._wind[2] = self.WINDTOLEFT
                    self._wind[0] = self._wind[0] +self._wind_to_move
                    self._wind[1] = self._wind[1] -self._wind_to_move
                else:
                    if self._wind[0] < -40:
                        self._wind[2] = self.WINDTORIGHT
                    self._wind[0] = self._wind[0] -self._wind_to_move
                    self._wind[1] = self._wind[1] +self._wind_to_move
                self.image.fill(self._sunset_colors.pop())
                self.image.blit(self._cloudy_surf, (self._wind[:2]))
                if self._sun_coord:
                    self.image.blit(self._sun_img, self._sun_coord.pop())
            else:
                self.image.blit(self.endtext_1, (self.display_size[0]//2-self.endtext_1.get_size()[0]//2, 100))
                self.image.blit(self.endtext_2, (self.display_size[0]//2-self.endtext_2.get_size()[0]//2, 500))


class Avatar(pygame.sprite.Sprite):

    char_images_pathdir = "postit_rush/asset/graphic/char/"
    images_path = {
        "cat": char_images_pathdir + 'cat.png',
        "boy": char_images_pathdir + 'boy.png',
        "horn": char_images_pathdir + 'horn.png',
        "pink": char_images_pathdir + 'pink.png',
        "princess": char_images_pathdir + 'princess.png',
    }

    def __init__(self, initial_position, char_nick=None):
        super(Avatar, self).__init__()
        self.display_size = pygame.display.get_surface().get_size()
        if not char_nick:
            image_path = random.choice(Avatar.images_path.values())
        else:
            image_path = Avatar.images_path[char_nick]
        self.image = pygame.image.load_extended(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.SPEED = self.current_speed = 7
        self.blocks_in_collision = None
        self.gems = []
        self.traveled = 0

        self._shake_clock = pygame.time.Clock()
        self._shake_elapsed = 0
        self._verse = -1
        self._px_to_shake = 1

        self._upset_input = False

        self.star = None
        self.bug = None

    def update(self):
        self._shake_elapsed += self._shake_clock.tick()
        if self._shake_elapsed >= 150:
            self.rect.centery += self._px_to_shake * self._verse
            self._shake_elapsed = 0
            self._verse = -self._verse
        self._upset_input = False

    def apply_effects(self):
        self.current_speed = self.SPEED
        if not self.star:
            if self.blocks_in_collision:
                for block in self.blocks_in_collision:
                    self.current_speed += block.speed
                    block.play_sfx()
                if self.current_speed < 1:
                    self.current_speed = 1
            for gem in self.gems:
                gem.drug_avatar(self)
            if self.bug:
                self.current_speed = 0
                if self.rect.right <= self.display_size[0]:
                   self.rect.centerx += 1
        elif self.bug:
            self.bug = None
        self.traveled += self.current_speed

    def blocks_handler(self, blocks):
        self.blocks_in_collision = pygame.sprite.spritecollide(self, blocks, False)

    def gems_handler(self, gems):
        for gem in self.gems:
            gem.age += gem.clock.tick()
            if gem.age >= gem.ttl:
                self.gems.remove(gem)
        if not self.star:
            for gem in pygame.sprite.spritecollide(self, gems, True):
                self.gems.append(gem)

    def bug_n_star_handler(self, bug_n_star):
        collisions = pygame.sprite.spritecollide(self, bug_n_star, True)
        for stuff in collisions:
            if isinstance(stuff, _Bug):
                self.bug = stuff
            if isinstance(stuff, _Star):
                self.star = stuff
        if self.star:
            if self.star.age > self.star.ttl:
                self.star = None
            else:
                self.star.age += self.star.clock.tick()
        if self.bug:
            if self.bug.rect.left >= self.display_size[0]:
                self.bug = None


class _Block(pygame.sprite.Sprite):

    types = namedtuple('Types', ['CONCRETE', 'GRASS', 'DIRT', 'WOOD'])(0, 1, 2, 3)

    _block_img_pathdir = "postit_rush/asset/graphic/block/"
    _block_snd_pathdir = "postit_rush/asset/audio/block/"

    _property = {
        0: (_block_img_pathdir + "concrete.png", _block_snd_pathdir + "concrete.wav", -3),
        1: (_block_img_pathdir + "grass.png", _block_snd_pathdir + "grass.wav", +3),
        2: (_block_img_pathdir + "dirt.png", _block_snd_pathdir + "dirt.wav", -1),
        3: (_block_img_pathdir + "wood.png", _block_snd_pathdir + "wood.wav", -2),
    }

    def __init__(self, initial_position, type):
        super(_Block, self).__init__()
        self.display_size = pygame.display.get_surface().get_size()

        self.image = pygame.image.load_extended(_Block._property[type][0])
        self.speed = _Block._property[type][2]

        self.sfx = pygame.mixer.Sound(_Block._property[type][1])
        self.sfx_already_played = False

        self.rect = self.image.get_rect()
        self.rect.center = initial_position

    def update(self, avatar_speed):
        if self.rect.top <= self.display_size[1]:
            self.rect.centery = self.rect.centery + avatar_speed

    def play_sfx(self):
        if not self.sfx_already_played:
            self.sfx.play()
            self.sfx_already_played = True


class _Gem(pygame.sprite.Sprite):

    colors = namedtuple('Color', ['BLUE', 'GREEN', 'ORANGE'])(0, 1, 2)

    def _blue_callback(self, avatar):
        avatar._upset_input = True

    def _orange_callback(self, avatar):
        avatar.current_speed += 7

    def _green_callback(self, avatar):
        avatar.current_speed += 5

    _gem_img_pathdir = "postit_rush/asset/graphic/gem/"

    _property = {
        0: (_gem_img_pathdir + "blue.png", 8000, _blue_callback),
        1: (_gem_img_pathdir + "green.png", 3000, _green_callback),
        2: (_gem_img_pathdir + "orange.png", 3000, _orange_callback),
    }

    def __init__(self, initial_position, color):
        super(_Gem, self).__init__()
        self.display_size = pygame.display.get_surface().get_size()
        self.color = color
        self.image = pygame.image.load_extended(_Gem._property[color][0])
        self.age = 0
        self.ttl = _Gem._property[self.color][1]
        self.sfx = pygame.mixer.Sound('postit_rush/asset/audio/gem.wav')
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.clock = pygame.time.Clock()

    def update(self, avatar_speed):
        if self.rect.top <= self.display_size[1]:
            self.rect.centery += avatar_speed

    def kill(self):
        super(_Gem, self).kill()
        self.sfx.play()
        self.clock.tick()

    def drug_avatar(self, avatar):
        self._property[self.color][2](self, avatar)


class _Star(pygame.sprite.Sprite):

    def __init__(self, initial_position):
        super(_Star, self).__init__()
        self.display_size = pygame.display.get_surface().get_size()
        self.image = pygame.image.load_extended('postit_rush/asset/graphic/star.png')
        self.age = 0
        self.ttl = 7000
        self._y_speed = 10
        self.sfx = pygame.mixer.Sound('postit_rush/asset/audio/star.wav')
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self.clock = pygame.time.Clock()

    def update(self, avatar_speed):
        if self.rect.top <= self.display_size[1]:
            self.rect.centery += avatar_speed + self._y_speed

    def kill(self):
        super(_Star, self).kill()
        self.sfx.play()
        self.clock.tick()


class _Bug(pygame.sprite.Sprite):

    def __init__(self, y_coord):
        super(_Bug, self).__init__()
        self.display_size = pygame.display.get_surface().get_size()
        self.image = pygame.image.load_extended('postit_rush/asset/graphic/bug.png')
        self._x_speed = 1
        self.sfx = pygame.mixer.Sound('postit_rush/asset/audio/bug.wav')
        self.rect = self.image.get_rect()
        self.rect.center = (-self.rect.width, y_coord)
        self.sfx_already_played = False

    def update(self, avatar_speed):
        if self.rect.left <= self.display_size[0]:
            self.rect.centerx += self._x_speed
            self.rect.centery += avatar_speed

    def kill(self):
        self.play_sfx()

    def play_sfx(self):
        if not self.sfx_already_played:
            self.sfx.play()
            self.sfx_already_played = True