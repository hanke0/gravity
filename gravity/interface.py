# -*- coding: utf-8 -*-
import abc

from gravity.utils import create_mapped_meta_class


__all__ = (
    "Recording",
    "RecordingMap",
    "Extractor",
    "ExtractorMap",
    "Transform",
    "TransformMap",
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
    def update(self, **kwargs):
        """update records values"""
        raise NotImplementedError

    @abc.abstractmethod
    def teardown(self):
        raise NotImplementedError


ExtractorMeta, ExtractorMap = create_mapped_meta_class("ExtractorMeta")


class Extractor(metaclass=ExtractorMeta):
    @abc.abstractmethod
    def extract(self, recording: Recording):
        raise NotImplementedError

    @abc.abstractmethod
    def teardown(self):
        raise NotImplementedError


PipeMeta, PipeMap = create_mapped_meta_class("PipeMeta")


class Pipe(metaclass=PipeMeta):
    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def teardown(self):
        raise NotImplementedError


TransformMeta, TransformMap = create_mapped_meta_class("TransformMeta")


class Transform(metaclass=TransformMeta):
    @abc.abstractmethod
    def transform(self, data):
        raise NotImplementedError

    @abc.abstractmethod
    def teardown(self):
        raise NotImplementedError


LoaderMeta, LoaderMap = create_mapped_meta_class("Loader")


class Loader(metaclass=LoaderMeta):
    @abc.abstractmethod
    def load(self, data):
        return

    @abc.abstractmethod
    def teardown(self):
        raise NotImplementedError
