import sys
from collections import OrderedDict

import yaml
import jinja2

from gravity.utils.utils import ensure_dict_structure
from gravity.errors import TemplateError


def map_representer(dumper, data):
    return dumper.represent_dict(data.items())


def map_constructor(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


SafeDumper = yaml.dumper.SafeDumper
DangerDumper = yaml.dumper.Dumper
SafeLoader = yaml.loader.SafeLoader
DangerLoader = yaml.loader.Loader

yaml.add_representer(dict, map_representer, Dumper=SafeDumper)
yaml.add_representer(OrderedDict, map_representer, Dumper=SafeDumper)
yaml.add_representer(dict, map_representer, Dumper=DangerDumper)
yaml.add_representer(OrderedDict, map_representer, Dumper=DangerDumper)


if sys.version_info < (3, 7):
    yaml.add_constructor("tag:yaml.org,2002:map", map_constructor, Loader=SafeLoader)
    yaml.add_constructor("tag:yaml.org,2002:map", map_constructor, Loader=DangerLoader)


class Task:
    def __init__(self, string: str) -> None:
        self._raw: str = string

    def check_template(self) -> dict:
        result: dict = yaml.safe_load(self._raw)
        ensure_dict_structure(
            result,
            {
                "name": str,
                "recording": {"class": str},
                "extract": {"class": str},
                "transform": [{"pipe": str}],
                "load": {"class": str},
            },
            absolute=False,
            error_class=TemplateError,
        )
        return result

    def render_result(self) -> dict:
        return yaml.safe_load(self.render_raw())

    def render_raw(self) -> str:
        var: dict = self.check_template().get("vars", {})
        if not var:
            return self._raw
        render_var: bool = False
        for k, v in var.items():
            if isinstance(v, str):
                var[k] = jinja2.Template(v).render(var)
            else:
                render_var = True
        if render_var:
            var: dict = yaml.safe_load(jinja2.Template(yaml.safe_dump(var)).render(var))
        raw: str = jinja2.Template(self._raw).render(var)
        return raw


if __name__ == "__main__":
    with open("../example/example.yaml", "rt") as f:
        t = Task(f.read())
        r = t.render_result()
    print(r["recording"])
