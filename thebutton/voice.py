import os

PREFIX = ".." # Work around the startup time for HDMI audio

class Voice:
    def say(self, message):
        if message:
            os.system("echo '{}{}' | festival --tts &".format(PREFIX, message))
