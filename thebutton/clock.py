from threading import Thread, Event
import time
from datetime import datetime as dt

class Clock:
    def __init__(self):
        self._wake_time = None
        self.event = Event()
        self.wake_time_set_event = Event()
        self.thread = Thread(target=Clock.clock_thread, args=[self])
        self.thread.daemon = True
        self.thread.start()
    
    @property
    def wake_time(self):
        return self._wake_time
    
    @wake_time.setter
    def wake_time(self, value):
        self._wake_time = value
        if value is None:
            self.wake_time_set_event.clear()
        else:
            self.wake_time_set_event.set()
    
    def clock_thread(self):
        while True:
            self.wake_time_set_event.wait()
            if self.wake_time is None:
                self.wake_time_set_event.clear() # Should not happen
            else:
                if dt.now() >= self.wake_time:
                    self.wake_time = None
                    self.event.set()
                else:   
                    self.sleep(min(10, (self.wake_time - dt.now()).total_seconds())) # Check at least every 10 seconds in case the wake time changes
    
    def sleep(self, seconds):
        time.sleep(seconds)


class ClockAndButton(Clock):
    def __init__(self, button):
        super().__init__()
        self.button = button
        self.button_pressed = False
    
    def sleep(self, seconds):
        if self.button.event.wait(seconds):
            self.button.event.clear()
            self.wake_time = None
            self.button_pressed = True
            self.event.set()

