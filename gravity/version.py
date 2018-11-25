from typing import NamedTuple

__version__ = "0.0.1"
__author__ = "ko-han"


def _get_version_info():
    major, minor, micro, *rs = __version__.split(".")
    if len(rs) == 2:
        releaselevel, serial = rs[0], int(rs[1])
    elif len(rs) == 1:
        releaselevel, serial = rs[0], 0
    else:
        releaselevel, serial = "final", 0
    return int(major), int(minor), int(minor), releaselevel, serial


class version_info(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


__version_info__ = version_info(*_get_version_info())

__all__ = ("__version__", "__version_info__", "__author__")
