import os
# from pydub import AudioSegment
# from pydub.playback import play
from playsound import playsound

#AudioSegment.ffmpeg = "C:\ffmpeg\bin\ffmpeg.exe"

print (os.getcwd())

class SoundManager:
    def __init__(self) -> None:
        pass

    def play_main_theme(self):
        # song = AudioSegment.from_mp3("tetris.mp3")
        # play(song)
        playsound("sounds/tetris.mp3", False)