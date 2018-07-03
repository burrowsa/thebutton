import os

PREFIX = "" # Add some full stops to Work around the startup time for HDMI audio if required

class Voice:
    def say(self, message):
        if message:
            os.system("echo '{}{}' | festival --tts &".format(PREFIX, message))
