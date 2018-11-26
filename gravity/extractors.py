# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from gravity.utils import create_mapped_meta_class




class SQLAlchemyExtractor(Extractor):
    def __init__(self, uri):
        self._engine: Engine = create_engine(uri)
        self._cursors = {}
        self._connections = {}

    def connect(self):
        queries = self.config["queries"]
        for query in queries:
            name = query["name"]
            query_file = query.get("file")
            if query_file:
                with open(query_file, "rt") as f:
                    query = f.read()
            else:
                query = query["query"]

            conn = self._engine.connect()
            self._connections[name] = conn
            cur = conn.execution_options(stream_results=True).execute(query)
            self._cursors[name] = cur
