if __name__ == "__main__":
    params = dict(name="thebutton",
        version="1.0.0",
        description="""A working model of BBC One's "The Button".""",
        author="Andrew Burrows",
        author_email="burrowsa@gmail.com",
        url="https://github.com/burrowsa/thebutton",
        packages=['thebutton'],
        license="BSD",
        long_description="""A working model of BBC One's "The Button".""",
        classifiers=[])

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup
    else:
        params['install_requires'] = []

    setup(**params)