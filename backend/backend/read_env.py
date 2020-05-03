import os
import re


class EnvironmentVariables:
    def __init__(self):
        self._values = {}

    def set(self, key, value):
        self._values[key] = value

    def get(self, key, default=None):
        return self._values.get(key, default)


def read_env(path, filename):
    """Pulled from Honcho code with minor updates, reads local default
    environment variables from an environment file
    """

    try:
        file_path = os.path.join(path, filename)
        with open(file_path) as file:
            content = file.read()
    except (IOError, TypeError):
        content = ""

    environment_variables = EnvironmentVariables()

    for line in content.splitlines():
        match_1 = re.match(r"\A([A-Za-z_0-9]+)=(.*)\Z", line)
        if match_1:
            key, val = match_1.group(1), match_1.group(2)
            match_2 = re.match(r"\A'(.*)'\Z", val)
            if match_2:
                val = match_2.group(1)
            match_3 = re.match(r'\A"(.*)"\Z', val)
            if match_3:
                val = re.sub(r"\\(.)", r"\1", match_3.group(1))
            if val.strip() != "":
                environment_variables.set(key, val.strip())

    return environment_variables
