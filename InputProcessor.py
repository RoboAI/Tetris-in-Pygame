import pygame

# TODO: this should be in its own file.
# TODO: problem: how would this file's functions be called from InputProcessor's file?
#------------------------------------------
class InputProcessor:
    def __init__(self) -> None:
        self.key_down_delegates = {}
        
        self.key_up_delegates = {}
        
    def add_keydown_callback(self, key, fn_callback):
        self.key_down_delegates.update({key: fn_callback})

    def add_keyup_callback(self, key, fn_callback):
        self.key_up_delegates.update({key: fn_callback})
    
    def get_delegate_keydown(self, key_pressed):
        return self.key_down_delegates.get(key_pressed, None)
    
    def get_delegate_keyup(self, key_released):
        return self.key_up_delegates.get(key_released, None)
    
    def process_inputs(self, *args) -> int:
        # loop through input-events
        for event in pygame.event.get():

            # Did the user click the window close button?
            if event.type == pygame.QUIT:
                return event.type

            # check for key-down
            if event.type == pygame.KEYDOWN:
    
                # get function delegate and call it
                fn = self.get_delegate_keydown(event.key)
                if( fn != None ):
                    fn(args[0])

            # check for key-up
            elif event.type == pygame.KEYUP:

                # get function delegate and call it
                fn = self.get_delegate_keyup(event.key)
                if( fn != None ):
                    fn(args[0])
#-------------------------------------------