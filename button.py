#!/usr/bin/env python3
from tkinter import *
import RPi.GPIO as GPIO
import time, os, threading, random
from datetime import timedelta, datetime as dt

BLUE = '#0e1a64'
LIGHT = 2
BUTTON = 4
RED = FALSE
GREEN = TRUE

class TheButton:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LIGHT, GPIO.OUT)
        GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(BUTTON, GPIO.FALLING)
        GPIO.add_event_callback(BUTTON, lambda pin: self.button_press(pin))
        GPIO.output(LIGHT, GREEN)
        self.tk = Tk()
        self.tk.attributes('-zoomed', True)
        self.is_fullscreen = True
        self.tk.attributes('-fullscreen', self.is_fullscreen)
        self.tk.configure(background=BLUE)
        self.frame = Frame(self.tk)
        self.frame.pack()
        self.message = StringVar()
        self.text = Label(self.frame,
                          fg='white',
                          bg='#0e1a64',
                          font=('Helvetica', 34),
                          height='9',
                          wraplength=self.tk.winfo_screenwidth() * 0.9,
                          textvariable=self.message)
        self.text.pack()
        self.tk.bind('<F11>', self.toggle_fullscreen)
        self.tk.bind('<Escape>', self.quit)
        self.then = None

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.tk.attributes('-fullscreen', self.is_fullscreen)
        return 'break'

    def quit(self, event=None):
        self.tk.destroy()
        return 'break'

    def button_press(self, pin):
        if GPIO.input(pin) == False and self.then is not None:
            then = self.then
            self.then = None
            then()
    
    def mainloop(self):
        self.tk.mainloop()

    def speak(self, message):
        #os.system('espeak -ven+f3 -k5 -s150 "{}"'.format(message))
        pass

    def display(self, message):
        self.message.set(message)

    def display_and_speak(self, message):
        self.display(message)
        self.speak(message)

    def red(self, then):
        GPIO.output(LIGHT, RED)
        time.sleep(0.5)
        self.then = then

    def green(self, then):
        GPIO.output(LIGHT, GREEN)
        time.sleep(0.5)
        self.then = then


wake_time = None
start_time = None
button = None


def schedule_next_challenge():
    global wake_time
    button.display("")
    wake_time = dt.now() + timedelta(seconds=3*60 + random.randint(0,7*60))

def finish_challenge():
    global start_time
    time_taken = dt.now() - start_time
    start_time = None
    button.display('Challenge Complete!\n\nYou took:\n{:02}:{:02}:{:02}'.format(time_taken.seconds // 3600, time_taken.seconds % 3600 // 60, time_taken.seconds % 60))
    button.speak('Challenge Complete!')
    button.green(then=schedule_next_challenge)

def start_challenge():
    global start_time
    start_time = dt.now()
    button.red(then=finish_challenge)

def display_challenge():
    button.green(then=None)
    button.display_and_speak("The first player to drink a glass of water in front of THE BUTTON is the winner. You must not start until THE BUTTON goes green. You must be sitting down") 
    time.sleep(5)
    start_challenge()

def play_challenge():
    button.red(then=display_challenge)

def game_thread():
    global wake_time
    while True:
        if wake_time is None:
            time.sleep(15)
        elif dt.now() >= wake_time:
            wake_time = None
            play_challenge()
        else:   
            time.sleep((wake_time - dt.now()).total_seconds())


def game():
    th = threading.Thread(target=game_thread)
    th.daemon = True
    th.start()
    schedule_next_challenge()


if __name__ == '__main__':
    button = TheButton()
    game()
    button.mainloop()

