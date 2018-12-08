import RPi.GPIO as GPIO
from threading import Event
from time import sleep
from datetime import timedelta, datetime as dt


BLUE = '#0e1a64'
GREEN = 2
RED = 3
BUTTON = 4
THREE_SECONDS = timedelta(seconds=3)


class Button:
    def __init__(self):
        self.event = Event()
        self.lastPressTime = dt.now()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GREEN, GPIO.OUT)
        GPIO.setup(RED, GPIO.OUT)
        GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(BUTTON, GPIO.FALLING)
        GPIO.add_event_callback(BUTTON, lambda pin: self.on_button_press(pin))
        self.green()

    def on_button_press(self, pin):
        if GPIO.input(pin) == False and dt.now() - self.lastPressTime > THREE_SECONDS:
            self.event.set()
            self.lastPressTime = dt.now()
            
    
    def red(self):
        GPIO.output(GREEN, False)
        GPIO.output(RED, True)

    def green(self):
        GPIO.output(RED, False)
        GPIO.output(GREEN, True)
