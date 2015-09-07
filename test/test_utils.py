import os
import inspect


def module_path(local_function):
    ''' returns the module path without the use of __file__.
    Requires a function defined locally in the module.
    from "http://stackoverflow.com/questions/729583/
    getting-file-path-of-imported-module"'''

    return os.path.abspath(inspect.getsourcefile(local_function))


TEST_DATA_PATH = os.path.join(
    os.path.split(module_path(module_path))[0], 'data')
