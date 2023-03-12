import pygame

from Globals import Globals
from InputProcessor import InputProcessor

gb = Globals

class ScreenMainMenu:
    def __init__(self) -> None:
        self.title_logo: pygame.Surface = None
        self.title_logo_rc = [0,0,0,0]
        self.start_text = "Start"
        self.controls_text = "Controls"
        self.selection = 0

        self.off_font_colour = "darkgray"
        self.on_font_colour = "white"
        self.start_rc = None
        self.controls_rc = None
        self.font: pygame.font.SysFont = None
        self.start_surface: pygame.Surface = None
        self.controls_surface: pygame.Surface = None
        self.font_family = "Comic Sans MS"
        self.font_size = 30

        self.init()
    
    def init_title(self):
        self.title_logo = pygame.image.load("images/title.png")

        scale = (gb.screen_width / self.title_logo.get_width()) / 1.5

        title_rect: pygame.Rect = pygame.Rect([
                        0, 
                        0, 
                        int(scale * self.title_logo.get_width()), 
                        int(scale * self.title_logo.get_height())])

        title_rect.move_ip(gb.screen_width / 2 - title_rect.width / 2, 25)

        self.title_logo = pygame.transform.scale(self.title_logo, title_rect.size)
        self.title_logo_rc = [title_rect.left, title_rect.top, title_rect.right, title_rect.bottom]          


    def init_menu(self):
        self.font = pygame.font.SysFont(self.font_family, self.font_size)

        self.start_surface = self.font.render(self.start_text, True, self.on_font_colour)
        self.controls_surface = self.font.render(self.controls_text, True, self.off_font_colour)
        
        #self.start_surface = pygame.Surface(0,0,0,0)
        #scale = self.start_surface.get_width() / self.start_surface.get_height()
        #text_rect = pygame.Rect(self.start_surface.get_rect())
        #text_rect.inflate_ip()
        #self.start_surface = pygame.transform.scale(self.start_surface, text_rect.size)

        self.start_rc = [gb.screen_width / 2 - self.start_surface.get_width() / 2, 
                         gb.screen_height / 2 + 50]
        self.controls_rc = [gb.screen_width / 2 - self.controls_surface.get_width() / 2, 
                         gb.screen_height / 2 + 100]
        
 
    def init(self):
        self.init_title()
        self.init_menu()
        self.highlight_menu(self.start_text)


    def highlight_menu(self, menu_name: str):
        if(menu_name.lower() == self.start_text.lower()):
            self.start_surface = self.font.render(self.start_text, True, self.on_font_colour)
            self.controls_surface = self.font.render(self.controls_text, True, self.off_font_colour)
        elif(menu_name.lower() == self.controls_text.lower()):
            self.start_surface = self.font.render(self.start_text, True, self.off_font_colour)
            self.controls_surface = self.font.render(self.controls_text, True, self.on_font_colour)
        else:
            pass


    def menu_hovered(self, selection: int):
        if(selection == 0):
            self.highlight_menu(self.start_text)
        elif(selection == 1):
            self.highlight_menu(self.controls_text)
        else:
            pass

    def keydown_down(self, *args):
        self.selection += 1
        if(self.selection >= 2):
            self.selection = 1
        self.menu_hovered(self.selection)

        return None

    def keydown_up(self, *args):
        self.selection -= 1
        if(self.selection < 0):
            self.selection = 0
        self.menu_hovered(self.selection)

        return None

    def keydown_return(self, *args):
        if(self.selection == 0):
            return self.start_text.lower()
        elif(self.selection == 1):
            return self.controls_text.lower()
        else:
            pass
        
        return 


    # def do_input(self, event: pygame.event) -> str:
    #     if(event.key == pygame.K_RETURN):
    #         if(self.selection == 0):
    #             return self.start_text.lower()
    #         elif(self.selection == 1):
    #             return self.controls_text.lower()
    #         else:
    #             pass
        
    #     if(event.key == pygame.K_DOWN):
    #         self.selection += 1
    #         if(self.selection >= 2):
    #             self.selection = 1
    #     elif(event.key == pygame.K_UP):
    #         self.selection -= 1
    #         if(self.selection < 0):
    #             self.selection = 0

    #     self.menu_hovered(self.selection)


    def draw(self, screen: pygame.Surface):
        # Fill the background
        screen.fill(gb.grid_bk_colour)

        # draw title
        screen.blit(self.title_logo, self.title_logo_rc)

        # draw buttons
        screen.blit(self.start_surface, self.start_rc)
        screen.blit(self.controls_surface, self.controls_rc)
