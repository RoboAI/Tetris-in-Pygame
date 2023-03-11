import pygame

# partially working.
# create SplashScreen() object, then start_animation()
class SplashScreen:
    def __init__(self, pygame: pygame, screen) -> None:
        self.pygame = pygame
        self.screen = screen
        self.sprites = []
        self.text: str
        self.rc: pygame.Rect
        self.rc_text: pygame.Rect
        self.frame_counter = 0
        self.frame_delay_counter = 0
        self.text_frame_counter = 0
        self.frame_delays = 0
        self.font = "Comic Sans MS"
        self.surface: pygame.Surface


    def start_animation(self, text, screen_size: pygame.Rect):
        self.text = text
        self.rc = screen_size
        self.rc_text = self.pygame.Rect(screen_size[2] / 2, screen_size[1] / 2, 500, 500)
        self.frame_counter = 0
        self.text_frame_counter = 0
        self.frame_delays = 30
        self.frame_delay_counter = 0
        self.font = pygame.font.SysFont(self.font, 80)
        self.surface = self.font.render(self.text, True, "black")


    def update_animation(self):
        if(self.text_frame_counter <= len(self.text)):
            if(self.frame_delay_counter >= self.frame_delays):
                self.text_frame_counter += 1
                self.frame_delay_counter = 0
            else:
                self.frame_delay_counter += 1

                self.surface = self.font.render(self.text[:self.text_frame_counter], True, "white")
                self.screen.blit(self.surface, self.rc)
            
            return True
        return False


