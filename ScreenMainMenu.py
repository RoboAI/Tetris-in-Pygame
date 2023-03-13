import collections
import pygame

from Globals import Globals
from InputProcessor import InputProcessor

gb = Globals

class ScreenMainMenu:
    MenuSelection = collections.namedtuple("MenuItem", ["name", "surface", "rect", "selected"])
    OFFSET_FROM_CENTER: float = 50
    SELECTION_SPACING: float = 10

    def __init__(self) -> None:
        self.title_logo: pygame.Surface = None
        self.title_logo_rc = [0,0,0,0]
        self.menu_selections = ["Start", "Controls", "Credits"]
        self.menu_dict = {}
        self.selection: int = 0

        self.off_font_colour = "darkgray"
        self.on_font_colour = "white"
        self.font: pygame.font.SysFont = None
        self.font_family = "Comic Sans MS"
        self.font_size = 30

        self.init()


    def init(self):
        self.init_title()
        self.init_menu()
        self.highlight_menu(self.menu_selections[self.selection])

    # setup title-logo
    def init_title(self):
        # load the title image
        self.title_logo = pygame.image.load("images/title.png")

        # calculate scale factor to fit in screen
        scale = (gb.screen_width / self.title_logo.get_width()) / 1.5

        # fill the rect with the scale-factors
        self.title_logo_rc  = pygame.Rect([
                        0, 
                        0, 
                        int(scale * self.title_logo.get_width()), 
                        int(scale * self.title_logo.get_height())])

        # move to center of the screen
        self.title_logo_rc.move_ip(gb.screen_width / 2 - self.title_logo_rc.width / 2, 25)

        # scale the image with calculated scaled-rect
        self.title_logo = pygame.transform.scale(self.title_logo, self.title_logo_rc.size)
        #self.title_logo_rc = [title_rect.left, title_rect.top, title_rect.right, title_rect.bottom]          


    # setup menu selections
    def init_menu(self):
        # setup font
        self.font = pygame.font.SysFont(self.font_family, self.font_size)

        # setup surfaces for all menus
        for i in range(len(self.menu_selections)):
            surface = self.font.render(self.menu_selections[i], True, self.off_font_colour)
        
            # setup each menu's rect
            rect = surface.get_rect()
            r = pygame.Rect(
                gb.screen_width / 2 - rect.width / 2, 
                gb.screen_height / 2 - rect.height / 2 + (i * rect.height) + (i * ScreenMainMenu.SELECTION_SPACING) + ScreenMainMenu.OFFSET_FROM_CENTER,
                gb.screen_width / 2 + rect.width / 2, 
                gb.screen_height / 2 + rect.height + (i * rect.height) + (i * ScreenMainMenu.SELECTION_SPACING) + ScreenMainMenu.OFFSET_FROM_CENTER )
        
            # create new updated tuple
            new_menu_item = ScreenMainMenu.MenuSelection(self.menu_selections[i], surface, r, False)

            # add new tuple to dictionary
            self.menu_dict.update({self.menu_selections[i] : new_menu_item})


    # highlight menu
    def highlight_menu(self, menu_name: str):
        # if menu doesn't exist then return
        if(menu_name not in self.menu_dict):
            return
        
        # if menu-to-select is already selected (highlighted)
        if(self.menu_dict.get(menu_name).selected == True):
            return
        
        # find menu to be highlighted
        menu_item_select = self.menu_dict.get(menu_name)

        # find menu to be de-highlighted
        menu_list = list(self.menu_dict.values())
        menu_items_unselect = [i for i in menu_list if i.selected == True]

        # draw highlighted version
        new_surface = self.font.render(menu_item_select.name, True, self.on_font_colour)
        
        # update dictionary
        menu_item_select = menu_item_select._replace(surface = new_surface, selected = True)
        self.menu_dict.pop(menu_name)
        self.menu_dict.update({menu_name : menu_item_select})

        # de-highlight others
        for item_name in menu_items_unselect:
            # render with 'off-colour'
            new_surface = self.font.render(item_name.name, True, self.off_font_colour)

            # update dictionary
            updated_item = self.menu_dict.get(item_name.name)._replace(surface = new_surface, selected = False)
            self.menu_dict.pop(item_name.name)
            self.menu_dict.update({item_name.name : updated_item})


    # key-down event
    def keydown_down(self, *args):
        # select next selection
        self.selection += 1

        # if selection is > number of selections, then loop back
        if(self.selection >= len(self.menu_selections)):
            self.selection = 0

        # highlight the selected menu
        self.highlight_menu(self.menu_selections[self.selection])


    # key-up event
    def keydown_up(self, *args):
        self.selection -= 1
        if(self.selection < 0):
            self.selection = len(self.menu_selections) - 1
        self.highlight_menu(self.menu_selections[self.selection])


    # key-return event
    def keydown_return(self, *args):
        return self.menu_selections[self.selection].lower()


    # draw all
    def draw(self, screen: pygame.Surface):
        # Fill the background
        screen.fill(gb.grid_bk_colour)

        # draw title
        screen.blit(self.title_logo, self.title_logo_rc)

        # draw buttons
        for item in self.menu_dict.values():
            screen.blit(item.surface, item.rect)
