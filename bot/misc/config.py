from abc import ABC
from typing import Final


class Config(ABC):
    CMD_PREFIX: Final = '/'
    DEBUG_MODE: Final = True
