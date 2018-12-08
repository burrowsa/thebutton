import os, random
from thebutton.parser import parse
from thebutton.standardwaitstep import StandardWaitStep


def load_all_challenges(path, randomise):
    all_files = os.listdir(path)
    if randomise:
        random.shuffle(all_files)
    else:
        all_files.sort()

    for filename in all_files:
        if filename.endswith(".json"):
            yield StandardWaitStep
            yield from parse(os.path.join(path, filename))

