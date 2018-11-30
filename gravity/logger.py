import sys
import logging

__all__ = ("GravityLogger",)


def new_handler():
    format_string = (
        "[%(asctime)s] [%(levelname)s] [%(process)s] " "[%(module)s:%(lineno)d] >> %(message)s"
    )
    fmt = logging.Formatter(format_string)
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(fmt)
    return handler


GravityLogger = logging.getLogger("gravity_logger")
GravityLogger.addHandler(new_handler())
