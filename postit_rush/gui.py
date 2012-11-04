import pygame

class Menu:

    def __init__(self, options, font_size, color, h_color, initial_position=(200,200)):
        self.options = options
        self.x, self.y = initial_position
        self.font = pygame.font.Font("postit_rush/asset/interface/font.ttf", font_size)
        self.cursor = 0
        self.color = color
        self.h_color = h_color

    def draw(self, surface):
        i = 0
        for option in self.options:
            if i == self.cursor:
                color = self.h_color
            else:
                color = self.color
            text = option[0]
            text_surf = self.font.render(text, True, color)
            y = self.y + i*self.font.get_height()
            surface.blit(text_surf, (self.x, y))
            i += 1

    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.cursor += 1
                if e.key == pygame.K_UP:
                    self.cursor -= 1
                if e.key == pygame.K_RETURN:
                    self.options[self.cursor][1]()
        if self.cursor > len(self.options)-1:
            self.cursor = 0
        if self.cursor < 0:
            self.cursor = len(self.options)-1

    def get_size(self):
        width = 0
        for option in self.options:
            text = option[0]
            text_surf = self.font.render(text, True, (0, 0, 0))
            if text_surf.get_width() > width:
                width = text_surf.get_width()
        height = len(self.options)*self.font.get_height()
        return (width, height)

    def set_topleft(self, topleft):
        self.x, self.y = topleft