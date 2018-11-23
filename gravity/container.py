# -*- coding: utf-8 -*-
import typing
import pandas as pd
from sqlalchemy import create_engine

if typing.TYPE_CHECKING:
    from typing import MutableMapping, AnyStr
    from ._type import DataSourceType, DataFrameType, EngineType, Engine


__all__ = ("DataSource", "DataSourceMap", "DataSourceMeta")


class Container:
    def __init__(self, data):
        self._data: MutableMapping[AnyStr, pd.DataFrame] = data

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, item):
        return item in self._data


class StatError(RuntimeError):
    pass


class DataSourceMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        DataSourceMap.register(cls)
        return cls


class Map(dict):
    def __setitem__(self, key: object, value: object) -> None:
        raise NotImplementedError

    def register(self, cls: DataSourceMeta) -> None:
        key = cls.__name__
        super().__setitem__(key, cls)


DataSourceMap = Map()


class DataSource(metaclass=DataSourceMeta):
    default_container = Container

    def __init__(
        self, config: MutableMapping, container: MutableMapping = None
    ) -> None:
        self.config = config
        self._closed = True
        self._connected = False
        self.container = self.default_container({}) if container is None else container

    def connect(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def fetch_next(self):
        """if finish, return None"""
        raise NotImplementedError

    def fetch_all(self):
        raise NotImplementedError

    @property
    def closed(self):
        return self._closed

    @closed.setter
    def closed(self, value):
        self._closed = bool(value)

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = bool(value)

    def __iter__(self):
        if self.closed:
            raise StatError("data source is closed")
        s = self.fetch_next()
        while s is not None:
            yield s
            s = self.fetch_next()

    def __next__(self):
        if self.closed:
            raise StatError("data source is closed")
        s = self.fetch_next()
        while s is not None:
            return s
        raise StopIteration

    def __str__(self):
        return "%s(connected=%s, closed=%s)" % (
            self.__class__.__name__,
            self.connected,
            self.closed,
        )


class SQLAlchemyDataSource(DataSource):
    def __init__(self, config, container=None):
        super().__init__(config)
        self._engine: Engine = create_engine(config["uri"])
        self._cursors = {}
        self._connections = {}
    
    def connect(self):
        if self.connect:
            raise StatError("already connect")
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
            

    def close(self):
        return

    def fetch_next(self):
        return

    def fetch_all(self):
        return
