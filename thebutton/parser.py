import json
from thebutton.genericstep import GenericStep
from thebutton.steps import step_factories


current_filename = None


def parse(filename):
    global current_filename
    current_filename = filename
    try:
        with open(filename) as f:
            parsed = json.load(f)

        if not isinstance(parsed, list):
            raise TypeError("Expected root element to be a list in '{}'".format(filename))

        return list(parse_element(parsed))
    finally:
        current_filename = None


def parse_element(element):
    if isinstance(element, list):
        for i in element:
            yield from parse_element(i)
    elif isinstance(element, str):
        element = element.strip()
        if element.startswith("!"):
            factory_name, *args = element.split(":")
            factory_name = factory_name[1:].strip().lower()
            if factory_name not in step_factories:
                raise ValueError("Unknown step type: '{}'".format(factory_name))
            yield from step_factories[factory_name](*[a.strip() for a in args])
        else:
            yield GenericStep(text=element)
    elif isinstance(element, dict):
        yield GenericStep(**element)
    else:
        raise TypeError("Unexpected type '{}' found in '{}'".format(type(element), current_filename))
