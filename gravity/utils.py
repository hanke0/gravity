# -*- coding: utf-8 -*-


class Map(dict):
    def __setitem__(self, key: object, value: object) -> None:
        raise NotImplementedError

    def register(self, cls: type) -> None:
        key = cls.__name__
        super().__setitem__(key, cls)

    def __str__(self):
        return "%s%s" % (self.__class__.__name__, super().__str__())


_meta_class_define_string = """
class {}(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        map.register(cls)
        return cls
"""


def create_mapped_meta_class(name):
    """create a class with a meta class that save it's class to a map
    
    :return:
    """
    local = {"map": Map()}
    exec(_meta_class_define_string.format(name), local, local)
    return local[name], local["map"]


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
            query = "CREATE INDEX %s__%s_index ON %s (%s)" % (
                table,
                field,
                table,
                field,
            )
            logging.info("RUN: %s", query)
            r = engine.execute(query)
            r.close()
