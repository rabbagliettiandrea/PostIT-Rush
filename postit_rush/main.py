from __future__ import division
import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from postit_rush import gui
from postit_rush.game import World, Avatar
from postit_rush.input import CameraInput, KeyboardInput
import sys

VERSION = "0.1 ALPHA"

class Main():

    def __init__(self):
        pygame.init()
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.display_size = (1000, 700)
        display_bitsize = 32
        self.display = pygame.display.set_mode(self.display_size, DOUBLEBUF | HWSURFACE, display_bitsize)
        self.FPS_limit = 30
        self.clock = pygame.time.Clock()
        self.keyboard = KeyboardInput()
        try:
            self.camera = CameraInput()
        except:
            self.camera = None
        self.music = pygame.mixer.Sound("postit_rush/asset/audio/music.wav")
        self.music.play(-1)

    def game(self, input_dev):
        self.input_dev = input_dev
        world = World(self.display_size[1]*30)
        avatar = Avatar( map(lambda x: x//2, self.display_size) )

        go = True
        while go:
            self.clock.tick(self.FPS_limit)
            for ev in pygame.event.get( (QUIT, KEYDOWN) ):
                if ev.type == QUIT:
                    self.exit()
                else:
                    if ev.key == K_ESCAPE:
                        input_dev.stop()
                        world.destroy()
                        go = False
            pygame.event.clear()

            self.display.blit(world.background.image, world.background.rect)
            world.blocks.draw(self.display)
            world.gems.draw(self.display)
            world.bug_n_star.draw(self.display)
            self.display.blit(avatar.image, avatar.rect)

            world.blocks.update(avatar.current_speed)
            world.gems.update(avatar.current_speed)
            world.bug_n_star.update(avatar.current_speed)
            input_dev.set_x_axis(avatar)
            avatar.update()
            world.background.update(avatar.traveled)
            avatar.blocks_handler(world.blocks)
            avatar.gems_handler(world.gems)
            avatar.bug_n_star_handler(world.bug_n_star)
            avatar.apply_effects()

            pygame.display.set_caption('PostIT Rush [%d fps]' % self.clock.get_fps())
            pygame.display.flip()

        input_dev.stop()
        return

    def menu(self):

        def start_w_keyboard():
            self.game(self.keyboard)

        def start_w_camera_nokey():
            self.camera.simulate_keyboard = False
            self.game(self.camera)

        def start_w_camera_key():
            self.camera.simulate_keyboard = True
            self.game(self.camera)

        def do_nothing():
            pass

        if self.camera:
            options = [ ("Start game (camera - keyboard behavior) CHOOSE THIS!", start_w_camera_key),
                        ("Start game (camera - following you) DEBUG PURPOSE ONLY", start_w_camera_nokey),
                        ("Start game (keyboard)", start_w_keyboard),
                        ("Exit", self.exit) ]
        else:
            options = [ ("Start game (keyboard)", start_w_keyboard),
                        ("Camera input's not available", do_nothing),
                        ("Exit", self.exit) ]

        menu = gui.Menu(options, 28, THECOLORS['blue'], THECOLORS['white'])
        menu_position = (self.display_size[0]//2-menu.get_size()[0]//2+30, self.display_size[1]*0.7)
        menu.set_topleft(menu_position)
        bg_img = pygame.image.load_extended("postit_rush/asset/interface/bg.png")
        ver_font = pygame.font.Font("postit_rush/asset/interface/font.ttf", 22)
        ver_text = ver_font.render(VERSION, True, THECOLORS['black'])
        go = True
        while go:
            self.clock.tick(self.FPS_limit)
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    go = False
            pygame.event.clear()
            self.display.blit(bg_img, (0,0))
            self.display.blit(ver_text, (self.display_size[0]-ver_text.get_size()[0]-20, 20))
            menu.draw(self.display)
            menu.update(events)
            pygame.display.set_caption('PostIT Rush [%d fps]' % self.clock.get_fps())
            pygame.display.flip()

        return 0

    def show_slide(self, filename):
        bg_img = pygame.image.load_extended(filename)
        go = True
        while go:
            self.clock.tick(self.FPS_limit)
            events = pygame.event.get()
            for e in events:
                if e.type == KEYDOWN and e.key == K_SPACE:
                    go = False
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    self.exit()
            pygame.event.clear()
            self.display.blit(bg_img, (0,0))
            pygame.display.set_caption('PostIT Rush [%d fps]' % self.clock.get_fps())
            pygame.display.flip()

        return 0

    def exit(self):
        sys.exit(0)