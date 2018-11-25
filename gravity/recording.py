# -*- coding: utf-8 -*-
import abc

from gravity.utils.utils import create_mapped_meta_class

RecordingMeta, RecordingMap = create_mapped_meta_class("RecordingMeta")


class Recording(metaclass=RecordingMeta):
    @abc.abstractmethod
    def get(self):
        raise NotImplementedError

    @abc.abstractmethod
    def save(self):
        raise NotImplementedError


class ContentRecording(Recording):
    def __init__(self, uri, database, collection, content):
        return

    def get_recording(self):
        return

    def save_recording(self):
        return

    def format(self, queries):
        return
