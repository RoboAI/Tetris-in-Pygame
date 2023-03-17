import os
# from pydub import AudioSegment
# from pydub.playback import play
from playsound import playsound
from pygame import mixer

#AudioSegment.ffmpeg = "C:\ffmpeg\bin\ffmpeg.exe"

# print (os.getcwd())


class SoundManager:
    def __init__(self) -> None:
        mixer.init() #Initialzing pyamge mixer
        #mixer.music.load("sounds/tetris-swing.ogg") #Loading Music File
        pass

    def play_main_theme(self):
        #playsound("sounds/tetris-swing.aac", False)
        #mixer.music.play() #Playing Music with Pygame (.ogg)
        pass

    def stop_main_theme(self):
        mixer.music.stop()

    def play_rows_cleared(self):
        playsound("sounds/burst-decent.aac", False)

    def play_speed_falling(self):
        playsound("sounds/rows_cleared4.wav", False)
        pass

    def play_touch_down(self):
        playsound("sounds/rows_cleared4.wav", False)

    def play_game_over(self):
        playsound("sounds/game-over.aac", False)
        pass