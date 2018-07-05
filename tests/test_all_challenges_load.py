from thebutton.loader import load_all_challenges
import os


def test_all_challenges_load():
    for challenge in load_all_challenges(os.path.join(os.path.dirname(os.path.dirname(__file__)), "challenges")):
        pass
