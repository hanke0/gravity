# -*- coding: utf-8 -*-

from gravity.utils.utils import create_mapped_meta_class


QueryMeta, QueryMap = create_mapped_meta_class("QueryMeta")


class Query(metaclass=QueryMeta):
    def format(self, record):
        return
