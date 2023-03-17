import pygame
from Globals import Globals

gb = Globals

# draws the game-over banner
class ArtGameOver:
    def __init__(self) -> None:
        self.font: pygame.font
        self.surface: pygame.Surface
        self.banner_rc: pygame.Rect
        self.text_rc: pygame.Rect

        self.init()

    def init(self):
        self.font = pygame.font.SysFont(gb.game_main_font, 40)
        self.surface = self.font.render('Game Over', True, gb.game_over_font_colour)
        self.banner_rc = pygame.Rect(gb.grid_actual_rect[0], 
                                     gb.grid_actual_rect[3] / 2 - self.surface.get_height() / 2,
                                     gb.grid_width, 
                                     self.surface.get_height())

        self.text_rc = pygame.Rect(self.banner_rc.left + (self.banner_rc.width / 2 - self.surface.get_width() / 2),
                                   self.banner_rc.top + (self.banner_rc.height / 2 - self.surface.get_height() / 2),
                                   self.surface.get_width(),
                                   self.surface.get_height())

    def draw(self, screen):
        pygame.draw.rect(screen, "black", self.banner_rc)
        screen.blit(self.surface, self.text_rc)