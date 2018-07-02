import os, random
from thebutton.parser import parse
from thebutton.standardwaitstep import StandardWaitStep


def load_all_challenges(path):
    all_files = os.listdir(path)
    random.shuffle(all_files)
    for filename in all_files:
        if filename.endswith(".json"):
            yield StandardWaitStep
            yield from parse(os.path.join(path, filename))

