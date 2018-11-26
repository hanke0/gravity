# -*- coding: utf-8 -*-
import abc

from gravity.utils import create_mapped_meta_class


__all__ = (
    "Recording",
    "RecordingMap",
    "Extractor",
    "ExtractorMap",
    "Pipe",
    "PipeMap",
    "Loader",
    "LoaderMap",
)

RecordingMeta, RecordingMap = create_mapped_meta_class("RecordingMeta")


class Recording(metaclass=RecordingMeta):
    """ Persistence record the etl result, if you wan't run it again.
    
    a record could be any thing that extractor or loader could handle with.
    this means a extractor class and a loader class are bound with specific recording class,
    at least bound with classes whose methods return same records scheme.
    """

    @abc.abstractmethod
    def retrieve(self):
        """retrieve or fetch a record."""
        raise NotImplementedError

    @abc.abstractmethod
    def keep(self):
        """keep or save record to persistence level."""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        """update records values"""
        raise NotImplementedError


ExtractorMeta, ExtractorMap = create_mapped_meta_class("ExtractorMeta")


class Extractor(metaclass=ExtractorMeta):
    def extract(self, recording):
        raise NotImplementedError


PipeMeta, PipeMap = create_mapped_meta_class("PipeMeta")


class Pipe(metaclass=PipeMeta):
    pass


LoaderMeta, LoaderMap = create_mapped_meta_class("Loader")


class Loader(metaclass=LoaderMeta):
    pass
