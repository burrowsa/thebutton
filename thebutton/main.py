from threading import Thread
from thebutton.loader import load_all_challenges
from thebutton.display import Display
from thebutton.button import Button
from thebutton.voice import Voice
from thebutton.clock import Clock, ClockAndButton


def game_thread(state):
    for challenge in load_all_challenges(state.challenges_path, state.randomise):
        challenge.run(state)
    state.display.show("All Challenges Completed")


def game(state):
    th = Thread(target=game_thread, args=[state])
    th.daemon = True
    th.start()


def main(challenges_path):
    class State:
        pass
    state = State() # Bag of state
    state.start_time = None
    state.challenges_path = challenges_path
    state.randomise = True
    state.display = Display()
    state.voice = Voice()
    state.button = Button()
    state.clock = Clock()
    state.clock_and_button = ClockAndButton(state.button)
    game(state)
    state.display.mainloop()
