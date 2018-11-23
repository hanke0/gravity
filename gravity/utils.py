# -*- coding: utf-8 -*-


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