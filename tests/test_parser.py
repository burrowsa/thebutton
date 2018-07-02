from thebutton.parser import parse_element, parse
from thebutton.genericstep import GenericStep
from thebutton.steps import ChallengeComplete
from unittest.mock import patch, sentinel, mock_open
from contextlib import contextmanager
import pytest


def test_parse():
    with patch("thebutton.parser.open", mock_open(read_data="""[ "hello" ]""")):
        result = parse(sentinel.filename)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].text == "hello"


def test_parse_not_a_list():
    with patch("thebutton.parser.open", mock_open(read_data="""{ "hello" : "world" }""")):
        with pytest.raises(TypeError) as err:
            parse(sentinel.filename)

    assert str(err.value) == "Expected root element to be a list in '{}'".format(sentinel.filename)


def test_parse_element_single_string():
    result = list(parse_element("hello"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].text == "hello"


def test_parse_element_list_of_one_string():
    result = list(parse_element(["hello"]))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].text == "hello"


def test_parse_element_list_of_strings():
    result = list(parse_element(["hello", "world"]))
    assert len(result) == 2
    assert isinstance(result[0], GenericStep)
    assert result[0].text == "hello"
    assert isinstance(result[1], GenericStep)
    assert result[1].text == "world"


def test_parse_element_nested_lists_of_strings():
    result = list(parse_element([["hello", [["world"]]]]))
    assert len(result) == 2
    assert isinstance(result[0], GenericStep)
    assert result[0].text == "hello"
    assert isinstance(result[1], GenericStep)
    assert result[1].text == "world"


def test_parse_element_bang_red():
    result = list(parse_element("!red"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].text is None
    assert result[0].colour == "red"


def test_parse_element_bang_red():
    result = list(parse_element("!green"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].text is None
    assert result[0].colour == "green"


def test_parse_element_bang_start():
    result = list(parse_element("!start"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].start == True


def test_parse_element_bang_start():
    result = list(parse_element("!button"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].wait_for_press == True


def test_parse_element_bang_wait_10():
    result = list(parse_element("!wait:10"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].time == 10


def test_parse_element_bang_wait_30():
    result = list(parse_element("!wait:30"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].time == 30


def test_parse_element_bang_red_upper():
    result = list(parse_element("!RED"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].text is None
    assert result[0].colour == "red"


def test_parse_element_bang_red_leading_spaces():
    result = list(parse_element(" !red"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].text is None
    assert result[0].colour == "red"


def test_parse_element_bang_red_trailing_spaces():
    result = list(parse_element("!red "))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].text is None
    assert result[0].colour == "red"


def test_parse_element_bang_red_leading_and_trailing_spaces():
    result = list(parse_element(" !red "))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].text is None
    assert result[0].colour == "red"


def test_parse_element_bang_red_space_after_bang():
    result = list(parse_element("! red"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].text is None
    assert result[0].colour == "red"


def test_parse_element_bang_wait_10_space_before_colon():
    result = list(parse_element("!wait :10"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].time == 10


def test_parse_element_bang_wait_10_space_after_colon():
    result = list(parse_element("!wait: 10"))
    assert len(result) == 1
    assert isinstance(result[0], GenericStep)
    assert result[0].time == 10


def test_parse_element_bang_challenge_complete():
    result = list(parse_element("!challenge complete"))
    assert len(result) == 1
    assert result[0] is ChallengeComplete


def test_parse_element_bang_challenge_complete_upper():
    result = list(parse_element("!Challenge Complete"))
    assert len(result) == 1
    assert result[0] is ChallengeComplete


def test_parse_element_bang_unknown():
    with pytest.raises(ValueError) as err:
        list(parse_element("!monkey"))
    assert str(err.value) == "Unknown step type: 'monkey'"


def test_parse_element_bang_unknown_upper():
    with pytest.raises(ValueError) as err:
        list(parse_element("!MonKEY"))
    assert str(err.value) == "Unknown step type: 'monkey'"


def test_parse_element_bang_unknown_spaces():
    with pytest.raises(ValueError) as err:
        list(parse_element(" ! monkey "))
    assert str(err.value) == "Unknown step type: 'monkey'"


def test_parse_element_bang_unknown_parameterised():
    with pytest.raises(ValueError) as err:
        list(parse_element("!monkey:100:200:hello:world:"))
    assert str(err.value) == "Unknown step type: 'monkey'"


def test_parse_element_bang_unknown_parameterised_spaces():
    with pytest.raises(ValueError) as err:
        list(parse_element(" ! monkey : 100 : 200 : hello : world : "))
    assert str(err.value) == "Unknown step type: 'monkey'"
