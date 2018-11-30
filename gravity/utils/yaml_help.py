# -*- coding: utf-8 -*-
import sys
from collections import OrderedDict

import yaml
import jinja2

__all__ = ("load_yaml_with_jinja2",)


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


def load_yaml_with_jinja2(string: str):
    origin = yaml.safe_load(string)
    var: dict = origin.get("vars", {})
    render_var: bool = False
    for k, v in var.items():
        if isinstance(v, str):
            var[k] = jinja2.Template(v).render(var)
        else:
            render_var = True
    if render_var:
        var: dict = yaml.safe_load(jinja2.Template(yaml.safe_dump(var)).render(var))
    raw: str = jinja2.Template(string).render(var)
    return yaml.safe_load(raw)
