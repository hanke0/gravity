import enum

from typing import Callable, MutableMapping, List
from operator import itemgetter

from gravity.utils import Singleton
from gravity.logger import GravityLogger

__all__ = ("EVENTS", "Event", "EventBus")


class Event:
    def __init__(self, type_):
        if type_ not in EVENTS:
            raise ValueError("unexpect event %s" % type_)
        self._event_type = type_

    @property
    def type(self):
        return EVENTS[self._event_type]

    def __repr__(self):
        return "Event(%s)(%s)" % (
            self.type,
            ", ".join("%s=%s" % (k, v) for k, v in self.__dict__.items() if not k.startswith("_")),
        )


class EVENTS(enum.Enum):
    STARTUP = "startup"
    RENDER = "render"
    EXTRACT = "extract"
    TRANSFORM = "transform"
    LOAD = "load"
    TEARDOWN = "teardown"


class EventBus(Singleton):
    def __init__(self) -> None:
        self._events_map: MutableMapping[str, List[Callable[[Event], bool], ...]] = {
            k: [] for k in vars(EVENTS).keys() if not k.startswith("_")
        }

    def push_event(self, event: Event):
        for i, run in self._events_map[event.type]:
            if not run(event):
                GravityLogger.debug("break when handle event=%s, func=(%s, %s)", event, i, run)
                break

    def register(self, event_type: str, func: Callable[[Event], bool], priority: int = 1):
        ls: list = self._events_map[EVENTS[event_type]]
        for _, run in ls:
            if run is func:
                raise ValueError("already register func %s" % func)
        v = (priority, func)
        ls.append(v)
        ls.sort(key=itemgetter(0))
        GravityLogger.debug("register event handle, type=%s, func=%s", EVENTS[event_type], func)
        return ls.index(v)

    def index(self, event_type: str, func: Callable[[Event], bool]):
        for i, (_, run) in enumerate(self._events_map[EVENTS[event_type]]):
            if run is func:
                return i
        raise ValueError("func not exists")


if __name__ == "__main__":
    bus = EventBus()
    print(bus.register(EVENTS.RENDER, lambda x: 1))
    print(bus.register(EVENTS.RENDER, lambda y: 1))
