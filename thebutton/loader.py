import os, random, pickle
from thebutton.parser import parse
from thebutton.standardwaitstep import StandardWaitStep


COMPLETED_CHALLENGES_PATH = "completed_challenges.pkl"


def load_completed():
    try:
        with open(COMPLETED_CHALLENGES_PATH, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return set()


def save_completed(completed):
    with open(COMPLETED_CHALLENGES_PATH, "wb") as f:
        return pickle.dump(completed, f)


def load_all_challenges(path, randomise):
    completed = load_completed()
    all_files = list(set(os.listdir(path)) - completed)

    if randomise:
        random.shuffle(all_files)
    else:
        all_files.sort()

    for filename in all_files:
        if filename.endswith(".json"):
            yield StandardWaitStep
            yield from parse(os.path.join(path, filename))
            completed.add(filename)
            save_completed(completed)
