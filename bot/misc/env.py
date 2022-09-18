import asyncio
import os
from abc import ABC
from typing import Final

import discord


class Env(ABC):
    TOKEN: Final = os.environ.get('Token', 'nan')
    VOICE: Final = int(os.environ.get('VoiceID', 'nan'))
    ROLE_ID: Final = int(os.environ.get('RolePlayersID', 'nan'))
    AFK: Final = int(os.environ.get('AFKVoice', 'nan'))
    CHANNEL: Final = int(os.environ.get('TextChannel', 'nan'))
    THREAD: Final = int(os.environ.get('TextThread', 'nan'))

    Packets = list()
    Server = None
    Role: discord.Role = None
    ImageManager = None
    LoopTask: asyncio.Task = None
