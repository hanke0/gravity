# -*- coding: utf-8 -*-
from typing import Type, TypeVar

from pandas import DataFrame

from .container import DataSourceMeta, DataSource


DataSourceType = TypeVar("DataSourceType", bound=DataSourceMeta)

DataFrameType = TypeVar("DataFrameType", bound=DataFrame)
