# -*- coding: utf-8 -*-
from gravity.utils import create_mapped_meta_class

RecordingMeta, RecordingMap = create_mapped_meta_class("RecordingMeta")


class Recording(metaclass=RecordingMeta):
    def get_recording(self):
        return

    def save_recording(self):
        return

    def format(self, queries):
        return


class ContentRecording(Recording):
    def __init__(self, uri, database, collection, content):
        return

    def get_recording(self):
        return

    def save_recording(self):
        return

    def format(self, queries):
        return


print(RecordingMeta, Recording, RecordingMap)
