from datetime import timedelta, datetime as dt


class GenericStep:
    def __init__(self, text=None, speech=None, time=None, colour=None, on_press=None, on_timeout=None, wait_for_press=None, start=None, stop=None):
        from thebutton.parser import parse_element
        self.text = text
        self.speech = speech
        self.time = int(time) if time is not None else None
        if colour is None or (isinstance(colour,str) and colour.lower() in ("red", "green")):
            self.colour = colour.lower() if colour is not None else None
        else:
            raise ValueError("Unknown colour for button '{}'".format(colour))
        self.on_press = list(parse_element(on_press)) if on_press is not None else None
        self.on_timeout = list(parse_element(on_timeout)) if on_timeout is not None else None
        self.wait_for_press = bool(wait_for_press)
        if self.on_press is not None and self.wait_for_press != True:
            raise ValueError("You should only set on_press if wait_for_press is set to True")
        if self.on_timeout is not None and self.time is None:
            raise ValueError("You should only set on_timeout if time is set")
        self.start = bool(start) if start is not None else None
        self.stop = bool(stop) if stop is not None else None

    @staticmethod
    def run_all(to_run, state):
        if to_run is not None:
            for i in to_run:
                i.run(state)
    
    def run(self, state):
        # should block until complete
        if self.text is not None:
            state.display.show(self.text)
            if self.speech is None:
                state.voice.say(self.text)
            else:
                state.voice.say(self.speech)
        
        if self.colour == "red":
            state.button.red()
        
        if self.colour == "green":
            state.button.green()
        
        if self.start == True:
            state.start_time = dt.now()
        
        if self.stop == True:
            state.start_time = None

        if self.time is not None and self.wait_for_press == True:
            state.clock_and_button.button_pressed = False
            state.clock_and_button.wake_time = dt.now() + timedelta(seconds=self.time)
            state.clock_and_button.event.clear()
            state.clock_and_button.event.wait()
            state.clock_and_button.event.clear()
            if state.clock_and_button.button_pressed:
                state.clock_and_button.button_pressed = False
                self.run_all(self.on_press, state)
            else:
                self.run_all(self.on_timeout, state)
        elif self.time is not None:
            state.clock.wake_time = dt.now() + timedelta(seconds=self.time)
            state.clock.event.clear()
            state.clock.event.wait()
            state.clock.event.clear()
            self.run_all(self.on_timeout, state)
        elif self.wait_for_press == True:
            state.button.event.clear()
            state.button.event.wait()
            state.button.event.clear()
            self.run_all(self.on_press, state)
