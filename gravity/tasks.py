# -*- encoding: utf-8 -*-
import time

import yaml

from gravity.utils import ensure_dict_structure, load_yaml_with_jinja2
from gravity.errors import TemplateError


class Task:
    def __init__(self, string: str) -> None:
        self._raw: str = string
        self._init_time = time.time()

    def _load(self) -> dict:
        result = load_yaml_with_jinja2(self._raw)
        ensure_dict_structure(
            result,
            {
                "name": str,
                "recording": {"class": str},
                "extract": {"class": str},
                "transform": {"class": str},
                "load": {"class": str},
            },
            absolute=False,
            error_class=TemplateError,
        )
        return result

    def begin(self):
        pass

    def teardown(self):
        pass


if __name__ == "__main__":
    with open("../example/example.yaml", "rt") as f:
        t = Task(f.read())
        r = t._load()
    print(r)
