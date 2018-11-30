# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager


__all__ = ("chdir", "ensure_dict_structure")


def get_table_index(table, engine):
    r = engine.execute("SHOW INDEX FROM %s" % table)
    d = []
    one = r.fetchone()
    while one:
        d.append(one["Column_name"])
        one = r.fetchone()
    r.close()
    return d


def _assure_index(engine, table, columns):
    for table in indexes:
        table_index = get_table_index(table, engine)
        for field in indexes[table]:
            if field in table_index:
                continue
            query = "CREATE INDEX %s__%s_index ON %s (%s)" % (table, field, table, field)
            logging.info("RUN: %s", query)
            r = engine.execute(query)
            r.close()


@contextmanager
def chdir(path):
    old_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_path)


def ensure_dict_structure(
    d: dict, structure: dict, absolute: bool = False, error_class: type = ValueError
) -> None:
    """
    :param d: need check dict
    :param structure: a structure dict is like this {"filed": int}
    :param absolute: do not allow extra keys
    :param error_class: a error class
    :return: None
    """
    if absolute and d.keys() - structure.keys():
        raise error_class("got unexpect keys %s" % (d.keys() - structure.keys()))
    for k, type_ in structure.items():
        if k not in d:
            raise error_class("missing key '%s'" % k)
        elif isinstance(type_, dict):
            ensure_dict_structure(d.get(k, {}), type_, absolute, error_class)
        elif isinstance(type_, list):
            if not isinstance(d[k], list):
                raise error_class("dict key %s should be %s, now got %s" % (k, list, d[k]))
            else:
                type_ = type_[0]
                for item in d[k]:
                    ensure_dict_structure(item, type_, absolute, error_class)
        elif not isinstance(d[k], type_):
            raise error_class("key %s should be %s, now got %s" % (k, type_, d[k]))
