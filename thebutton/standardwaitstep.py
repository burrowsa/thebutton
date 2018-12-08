from random import randint
from thebutton.genericstep import GenericStep

MIN_WAIT_SEC = 3*60
MAX_WAIT_SEC = 12*60

class StandardWaitStep:
    @staticmethod
    def run(state):
        GenericStep(text="", colour="green", time=randint(MIN_WAIT_SEC, MAX_WAIT_SEC), on_timeout=dict(colour="red", wait_for_press=True)).run(state)
