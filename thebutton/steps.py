from thebutton.genericstep import GenericStep
from datetime import datetime as dt


step_factories = {}


def step_factory(name):
    def step_factory_impl(fn):
        step_factories[name.lower()] = fn
        return fn
    return step_factory_impl


@step_factory("wait")
def wait(time):
    yield GenericStep(time=time)


@step_factory("red")
def red():
    yield GenericStep(colour="red")


@step_factory("green")
def green():
    yield GenericStep(colour="green")


@step_factory("start")
def start():
    yield GenericStep(start=True)


@step_factory("stop")
def start():
    yield GenericStep(stop=True)


@step_factory("button")
def button():
    yield GenericStep(wait_for_press=True)


class ChallengeComplete:
    @staticmethod
    def run(state):
        step = GenericStep(wait_for_press=True,
                    colour="green",
                    on_press="",
                    stop=True)
        if state.start_time is not None:
            time_taken = dt.now() - state.start_time
            hours = time_taken.seconds // 3600
            minutes = time_taken.seconds % 3600 // 60
            seconds = time_taken.seconds % 60
            if hours:
                step.text = "Challenge Complete!\n\nYou took:\n{:02}:{:02}:{:02}\n\nSend a photo of this screen to HQ then press the button.".format(hours, minutes, seconds)
                step.speech = "Challenge Complete! You took {} hours, {} minutes and {} seconds".format(hours, minutes, seconds)
            elif minutes:
                step.text = "Challenge Complete!\n\nYou took:\n{:02}:{:02}\n\nSend a photo of this screen to HQ then press the button.".format(minutes, seconds)
                step.speech = "Challenge Complete! You took {} minutes and {} seconds".format(minutes, seconds)
            else:
                step.text = "Challenge Complete!\n\nYou took:\n{}s\n\nSend a photo of this screen to HQ then press the button.".format(seconds)
                step.speech = "Challenge Complete! You took {} seconds".format(seconds)
        else:
            step.text = "Challenge Complete!\n\nPress the button to continue."
        step.run(state)



@step_factory("challenge complete")
def challenge_complete():
    yield ChallengeComplete


@step_factory("time up")
@step_factory("times up")
@step_factory("time's up")
def time_up():
    yield GenericStep(text="Time's up, you failed the challenge.",
                wait_for_press=True,
                colour="green",
                stop=True,
                on_press="")
