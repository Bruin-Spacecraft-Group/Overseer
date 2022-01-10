# -*- coding: utf-8 -*-
# @Author: p-chambers
# @Date:   2016-11-17 17:32:25
# @Last Modified by:   Paul Chambers
# @Last Modified time: 2017-05-10 22:03:57

__all__ = ["global_tools", "flight_tools", "simulator", "weather"]

from . import simulator
from . import weather

from .simulator import flight


import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
logging.basicConfig(level=logging.DEBUG)
logging.getLogger(__name__).addHandler(NullHandler())