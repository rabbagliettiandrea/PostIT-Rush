from __future__ import division
import pygame
import pygame.camera
from pygame.locals import *

class InputDevice(object):

    def __init__(self):
        self.display_size = pygame.display.get_surface().get_size()
        self.movement = self.display_size[0]//100

    def set_x_axis(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()


class KeyboardInput(InputDevice):

    def __init__(self):
        super(KeyboardInput, self).__init__()

    def set_x_axis(self, avatar):
        if avatar.bug:
            return
        keys_pressed = pygame.key.get_pressed()
        if avatar._upset_input:
            if keys_pressed[K_RIGHT]:
                if avatar.rect.centerx > self.movement:
                    avatar.rect.centerx -= self.movement
            if keys_pressed[K_LEFT]:
                if avatar.rect.centerx < self.display_size[0] - self.movement:
                    avatar.rect.centerx += self.movement
        else:
            if keys_pressed[K_RIGHT]:
                if avatar.rect.centerx < self.display_size[0] - self.movement:
                    avatar.rect.centerx += self.movement
            if keys_pressed[K_LEFT]:
                if avatar.rect.centerx > self.movement:
                    avatar.rect.centerx -= self.movement

    def stop(self):
        pass


class CameraInput(InputDevice):

    def __init__(self):
        super(CameraInput, self).__init__()
        pygame.camera.init()
        self.shrinked_size = (32, 24)
        self.cam_resolution = (640, 480)
        self.screen_percent_to_capture = 0.60
        self.ratio_x = self.display_size[0]/self.shrinked_size[0]
        self.cam_list = pygame.camera.list_cameras()
        self.cam = pygame.camera.Camera(self.cam_list[0], self.cam_resolution)
        self.simulate_keyboard = False
        self.avatar_upset_input = False
        self._snap_1 = None
        self._snap_2 = None
        self._old_diff = None

    def set_x_axis(self, avatar):
        if avatar.bug:
            return
        if not self._snap_1:
            self._snap_1 = self.get_snapshot(self.shrinked_size)
        self._snap_2 = self.get_snapshot(self.shrinked_size)
        diff = self.get_diff_surface(self._snap_1, self._snap_2)
        if not diff:
            if not self._old_diff:
                return None
            diff = self._old_diff
        else:
            self._old_diff = diff
        self._snap_1 = self._snap_2
        mask = pygame.mask.from_surface(diff)
        x_mask = int(self.display_size[0]-mask.centroid()[0]*self.ratio_x)
        self.avatar_upset_input = avatar._upset_input
        if self.simulate_keyboard:
            if x_mask > self.display_size[0] - (self.display_size[0]/5)*2:
                if avatar.rect.centerx < self.display_size[0] - self.movement:
                    avatar.rect.centerx += self.movement
            if x_mask < (self.display_size[0]/5)*2:
                if avatar.rect.centerx > self.movement:
                    avatar.rect.centerx -= self.movement
        else:
            avatar.rect.centerx = x_mask
#

    def stop(self):
        self.cam.stop()
        pygame.camera.quit()

    def get_diff_surface(self, surf_1, surf_2):
        diff_surf = pygame.Surface(self.shrinked_size, SRCALPHA)
        diff_surf.fill((0,0,0,0))
        pixel_in_surf = 0
        for y in xrange( int( self.shrinked_size[1]*self.screen_percent_to_capture ) ):
            for x in xrange(self.shrinked_size[0]):
                pos = (x, y)
                p1 = surf_1.get_at(pos)
                p2 = surf_2.get_at(pos)
                diff_pix = [abs(p1[0] - p2[0]), abs(p1[1] - p2[1]), abs(p1[2] - p2[2]), 255]
                avrg_pix = (diff_pix[0] + diff_pix[1] + diff_pix[2]) / 3
                if avrg_pix >= 35:
                    pixel_in_surf += 1
                    diff_surf.set_at(pos, diff_pix)
        if pixel_in_surf <= 15:
            return None
        return diff_surf

    def get_snapshot(self, size):
        tmp = pygame.surface.Surface(self.cam_resolution)
        self.cam.get_image(tmp)
        if self.cam_resolution != size:
            tmp_resized = pygame.surface.Surface(size)
            pygame.transform.scale(tmp, size, tmp_resized)
            tmp = tmp_resized
        if self.avatar_upset_input:
            tmp_flipped = pygame.transform.flip(tmp, True, False)
            tmp = tmp_flipped
        return tmp.copy()