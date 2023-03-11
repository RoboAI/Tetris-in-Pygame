import pygame
from Globals import Globals


gb = Globals

class ScoreBoard:
        def __init__(self, pygame, area_rc: pygame.Rect = pygame.Rect(0,0,100,100), 
                     font_family: str = "Comic Sans MS", font_size: int = 30) -> None:
            self.pygame = pygame
            self.drawing_rc = area_rc
            self.player_score: int = 0
            self.layers_score: int = 0
            self.player_score_title = "Score"
            self.layers_title = "Rows"

            self.titles_font_colour = "gray"
            self.scores_font_colour = "beige"
            self.player_score_font: pygame.font.SysFont = None
            self.layer_score_font: pygame.font.SysFont = None
            self.player_score_surface = None # pygame Surface
            self.layer_score_surface = None # pygame Surface
            self.font_family = font_family
            self.font_size = font_size
            
        def init_fonts(self, title_colour, scores_colour, layers_title: str, player_score_title: str):
            self.titles_font_colour = title_colour
            self.scores_font_colour = scores_colour
            self.layers_title = layers_title
            self.player_score_title = player_score_title

            self.layer_title_font = pygame.font.SysFont(self.font_family, self.font_size)
            self.score_title_font = pygame.font.SysFont(self.font_family, self.font_size)
            self.player_score_font = pygame.font.SysFont(self.font_family, self.font_size)
            self.layer_score_font = pygame.font.SysFont(self.font_family, self.font_size)

            self.set_texts(layers_title, player_score_title)
        
        def set_colour(self, title_colour, scores_colour):
             self.titles_font_colour = title_colour
             self.scores_font_colour = scores_colour

        def set_texts(self, layers_title: str, player_score_title: str):
            self.layers_title = layers_title
            self.player_score_title = player_score_title
            self.layer_title_surface = self.layer_title_font.render(self.layers_title, True, self.titles_font_colour)
            self.score_title_surface = self.score_title_font.render(self.player_score_title, True, self.titles_font_colour)
            self.update_player_score(self.player_score)
            self.update_layers_score(self.layers_score)

        def update_player_score(self, score: str):
            self.player_score = score
            self.player_score_surface = self.player_score_font.render(str(self.player_score), True, self.scores_font_colour)
        
        def update_layers_score(self, score: int):
            self.layers_score = score
            self.layer_score_surface = self.layer_score_font.render(str(self.layers_score), True, self.scores_font_colour)

        # TODO: this function should use the Rect that was given in the constructor
        def draw_texts(self, screen):
            screen.blit(self.layer_title_surface, gb.infobox_layer_title_xy)
            screen.blit(self.layer_score_surface, gb.infobox_layer_score_xy)
            screen.blit(self.score_title_surface, gb.infobox_score_title_xy)
            screen.blit(self.player_score_surface, gb.infobox_player_score_xy)
             

 